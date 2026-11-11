"""ALBERT sentiment experiments with fixed splits and validation selection."""

from copy import deepcopy
from pathlib import Path
from time import perf_counter
import gc
import hashlib
import os
import platform
import random
import sys
import threading

import numpy as np
import pandas as pd
import psutil
import torch
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
from torch import nn
from torch.utils.data import DataLoader, TensorDataset

LAB_DIR = Path(__file__).resolve().parent
ROOT = LAB_DIR.parents[1]
os.environ.setdefault('HF_HOME', str(ROOT / 'models' / 'huggingface'))
from transformers import AutoModel, AutoTokenizer
MODEL_ID = 'albert/albert-base-v2'
REVISION = '8e2f239c5f8a2c0f253781ca60135db913e5c80c'
SEED, BATCH_SIZE, EPOCHS = 42, 8, 2
DEVICE = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
sys.path.insert(0, str(ROOT / 'labs' / 'lab07'))
from transformer_block import TransformerBlock
from positional_encoding import PositionalEncoding


def seed_everything(seed=SEED):
    random.seed(seed)
    np.random.seed(seed)
    torch.manual_seed(seed)
    if torch.cuda.is_available():
        torch.cuda.manual_seed_all(seed)
    torch.set_num_threads(min(4, torch.get_num_threads()))


def get_tokenizer():
    return AutoTokenizer.from_pretrained(MODEL_ID, revision=REVISION)


def balanced_sample(frame, per_class):
    selected = pd.concat([frame[frame.label == label].sample(n=per_class, random_state=SEED)
                          for label in [0, 1]])
    return selected.sample(frac=1, random_state=SEED).reset_index(drop=True)


def load_splits():
    """IMDb 60/20/20 balanced CPU subsets; the original split is preserved."""
    data = ROOT / 'labs' / 'lab04' / 'data'
    splits = {name: balanced_sample(pd.read_csv(data / f'imdb_{name}.csv.gz'), count)
              for name, count in [('train', 300), ('validation', 100), ('test', 100)]}
    for frame in splits.values():
        assert not frame.text.isna().any() and set(frame.label) == {0, 1}
    sets = {name: set(frame.text.str.strip()) for name, frame in splits.items()}
    assert not (sets['train'] & sets['validation'] or sets['train'] & sets['test']
                or sets['validation'] & sets['test'])
    return splits


def training_subset(frame, fraction):
    """Nested, stratified subsets: the same class order is used at every fraction."""
    pieces = [frame[frame.label == label].sample(frac=1, random_state=SEED)
              for label in [0, 1]]
    selected = pd.concat([part.iloc[:int(len(part) * fraction)] for part in pieces])
    return selected.sample(frac=1, random_state=SEED).reset_index(drop=True)


def encoded_dataset(frame, tokenizer, length):
    encoded = tokenizer(frame.text.tolist(), padding='max_length', truncation=True,
                        max_length=length, return_tensors='pt')
    return TensorDataset(encoded['input_ids'], encoded['attention_mask'],
                         torch.tensor(frame.label.to_numpy(), dtype=torch.long))


def loader(dataset, shuffle=False):
    return DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=shuffle,
                      generator=torch.Generator().manual_seed(SEED), num_workers=0)


class PretrainedClassifier(nn.Module):
    def __init__(self, frozen=False):
        super().__init__()
        self.encoder = AutoModel.from_pretrained(MODEL_ID, revision=REVISION)
        self.classifier = nn.Linear(self.encoder.config.hidden_size, 2)
        self.frozen = frozen
        if frozen:
            self.encoder.requires_grad_(False)

    def train(self, mode=True):
        super().train(mode)
        if self.frozen:
            self.encoder.eval()
        return self

    def features(self, ids, mask):
        # ALBERT's pooler is a learned transformation of the [CLS] hidden state.
        return self.encoder(input_ids=ids, attention_mask=mask).pooler_output

    def forward(self, ids, mask):
        return self.classifier(self.features(ids, mask))


class ScratchClassifier(nn.Module):
    """Small Lab 07 block, random weights, the SAME ALBERT token IDs and budget."""
    def __init__(self, tokenizer):
        super().__init__()
        self.embedding = nn.Embedding(len(tokenizer), 128, padding_idx=tokenizer.pad_token_id)
        self.position = PositionalEncoding(128, 512)
        self.dropout = nn.Dropout(0.1)
        self.block = TransformerBlock(128, 4, 256, dropout=0.1)
        self.classifier = nn.Linear(128, 2)

    def forward(self, ids, mask):
        hidden = self.block(self.dropout(self.position(self.embedding(ids))), mask.bool())
        return self.classifier(hidden[:, 0])


def metrics(truth, prediction):
    return dict(accuracy=accuracy_score(truth, prediction),
                precision=precision_score(truth, prediction, zero_division=0),
                recall=recall_score(truth, prediction, zero_division=0),
                f1=f1_score(truth, prediction, zero_division=0))


def evaluate(model, data_loader, features=False):
    model.eval()
    truth, probabilities = [], []
    total_loss = 0.0
    with torch.no_grad():
        for batch in data_loader:
            batch = [tensor.to(DEVICE) for tensor in batch]
            logits = model(batch[0]) if features else model(batch[0], batch[1])
            labels = batch[-1]
            total_loss += nn.functional.cross_entropy(logits, labels, reduction='sum').item()
            truth.extend(labels.cpu().tolist())
            probabilities.extend(logits.softmax(-1).cpu().tolist())
    probabilities = np.array(probabilities)
    truth = np.array(truth)
    prediction = probabilities.argmax(1)
    return dict(truth=truth, prediction=prediction, probabilities=probabilities,
                confidence=probabilities.max(1), loss=total_loss / len(truth),
                metrics=metrics(truth, prediction))


class PeakMemory:
    """Sample process RSS (CPU); this includes the Python process and allocator."""
    def __enter__(self):
        self.process = psutil.Process()
        self.peak = self.process.memory_info().rss
        self.stop = threading.Event()
        def sample():
            while not self.stop.wait(0.05):
                self.peak = max(self.peak, self.process.memory_info().rss)
        self.thread = threading.Thread(target=sample, daemon=True)
        self.thread.start()
        if DEVICE.type == 'cuda':
            torch.cuda.reset_peak_memory_stats()
        return self

    def __exit__(self, *args):
        self.peak = max(self.peak, self.process.memory_info().rss)
        self.stop.set()
        self.thread.join()
        self.mib = (torch.cuda.max_memory_allocated() if DEVICE.type == 'cuda'
                    else self.peak) / 1024**2


def extract_features(model, data_loader):
    model.eval()
    vectors, labels = [], []
    with torch.no_grad():
        for ids, mask, target in data_loader:
            vectors.append(model.features(ids.to(DEVICE), mask.to(DEVICE)).cpu())
            labels.append(target)
    return TensorDataset(torch.cat(vectors), torch.cat(labels))


def train_experiment(splits, tokenizer, kind='finetuned', fraction=1.0, length=64):
    seed_everything()
    frame = training_subset(splits['train'], fraction)
    frames = dict(splits, train=frame)
    datasets = {name: encoded_dataset(part, tokenizer, length) for name, part in frames.items()}
    model = (ScratchClassifier(tokenizer) if kind == 'scratch'
             else PretrainedClassifier(frozen=kind == 'frozen')).to(DEVICE)
    learning_rate = {'scratch': 1e-3, 'frozen': 1e-3, 'finetuned': 2e-5}[kind]
    optimizer = torch.optim.AdamW([p for p in model.parameters() if p.requires_grad],
                                  lr=learning_rate, weight_decay=0.01)
    history, best_f1, best_state, best_epoch = [], -1, None, None
    with PeakMemory() as memory:
        if DEVICE.type == 'cuda':
            torch.cuda.synchronize()
        start = perf_counter()
        if kind == 'frozen':
            # Cache train/validation features once; extraction IS included in training time.
            training_data = {name: extract_features(model, loader(datasets[name]))
                             for name in ['train', 'validation']}
            training_model = model.classifier
        else:
            training_data = datasets
            training_model = model
        train_loader = loader(training_data['train'], shuffle=True)
        validation_loader = loader(training_data['validation'])
        for epoch in range(1, EPOCHS + 1):
            training_model.train()
            total = 0.0
            for batch in train_loader:
                batch = [tensor.to(DEVICE) for tensor in batch]
                optimizer.zero_grad(set_to_none=True)
                logits = (training_model(batch[0]) if kind == 'frozen'
                          else training_model(batch[0], batch[1]))
                loss = nn.functional.cross_entropy(logits, batch[-1])
                loss.backward()
                nn.utils.clip_grad_norm_(training_model.parameters(), 1.0)
                optimizer.step()
                total += loss.item() * len(batch[-1])
            val = evaluate(training_model, validation_loader, features=kind == 'frozen')
            history.append(dict(epoch=epoch, train_loss=total / len(frame),
                                validation_loss=val['loss'], validation_f1=val['metrics']['f1']))
            if val['metrics']['f1'] > best_f1:
                best_f1, best_epoch = val['metrics']['f1'], epoch
                best_state = {key: value.detach().cpu().clone()
                              for key, value in model.state_dict().items()}
            print(f'{kind} fraction={fraction} length={length} epoch={epoch} '
                  f'val_F1={val["metrics"]["f1"]:.4f}', flush=True)
        if DEVICE.type == 'cuda':
            torch.cuda.synchronize()
        elapsed = perf_counter() - start
    model.load_state_dict(best_state)
    test = evaluate(model, loader(datasets['test']))
    row = dict(model=kind, train_fraction=fraction, train_samples=len(frame),
               validation_samples=len(splits['validation']), test_samples=len(splits['test']),
               max_length=length, epochs=EPOCHS, best_epoch=best_epoch, seed=SEED,
               batch_size=BATCH_SIZE, learning_rate=learning_rate, optimizer='AdamW',
               parameters=sum(p.numel() for p in model.parameters()),
               trainable_parameters=sum(p.numel() for p in model.parameters() if p.requires_grad),
               validation_f1=best_f1, training_time_sec=elapsed,
               peak_memory_mib=memory.mib, memory_kind='CUDA allocated' if DEVICE.type == 'cuda' else 'process RSS',
               **test['metrics'])
    result = dict(row=row, history=history, test=test, fingerprints=split_fingerprints(splits))
    checkpoint = ROOT / 'checkpoints' / 'lab08'
    checkpoint.mkdir(parents=True, exist_ok=True)
    torch.save(dict(result=result, state=best_state), checkpoint / f'{kind}_{fraction}_{length}.pt')
    del best_state, optimizer
    gc.collect()
    return model, result


def restore_experiment(splits, tokenizer, kind, fraction, length, keep_model=False):
    """Resume our local runs; reported training times remain the original measurements."""
    path = ROOT / 'checkpoints' / 'lab08' / f'{kind}_{fraction}_{length}.pt'
    if not path.exists():
        return None
    # This file is created locally by train_experiment, not obtained from a third party.
    payload = torch.load(path, map_location='cpu', weights_only=False)
    result = payload['result']
    row = result['row']
    expected = dict(model=kind, train_fraction=fraction, max_length=length,
                    train_samples=len(training_subset(splits['train'], fraction)),
                    validation_samples=len(splits['validation']), test_samples=len(splits['test']),
                    batch_size=BATCH_SIZE, epochs=EPOCHS, seed=SEED)
    if any(row.get(key) != value for key, value in expected.items()):
        raise ValueError(f'Checkpoint configuration mismatch: {path.name}')
    if 'fingerprints' in result and result['fingerprints'] != split_fingerprints(splits):
        raise ValueError('Checkpoint split fingerprints do not match')
    assert np.array_equal(result['test']['truth'], splits['test'].label.to_numpy())
    model = None
    if keep_model:
        seed_everything()
        model = (ScratchClassifier(tokenizer) if kind == 'scratch'
                 else PretrainedClassifier(frozen=kind == 'frozen')).to(DEVICE)
        model.load_state_dict(payload['state'])
        model.eval()
    print(f'Restored {path.name}; original training time={row["training_time_sec"]:.2f}s', flush=True)
    return model, result


def load_amazon(splits):
    """Held-out product reviews: never used for training or model selection."""
    path = LAB_DIR / 'data' / 'amazon_cells_labelled.txt'
    if not path.exists():
        import io
        import urllib.request
        import zipfile
        url = 'https://archive.ics.uci.edu/static/public/331/sentiment+labelled+sentences.zip'
        archive = zipfile.ZipFile(io.BytesIO(urllib.request.urlopen(url, timeout=60).read()))
        name = next(n for n in archive.namelist() if n.endswith('/amazon_cells_labelled.txt'))
        path.parent.mkdir(exist_ok=True)
        path.write_bytes(archive.read(name))
    frame = pd.read_csv(path, sep='\t', names=['text', 'label'], quoting=3)
    frame = frame.drop_duplicates('text').reset_index(drop=True)
    imdb_texts = set(pd.concat(splits.values()).text.str.strip().str.lower())
    return frame[~frame.text.str.strip().str.lower().isin(imdb_texts)].reset_index(drop=True)


def hardware_info():
    return dict(device=str(DEVICE), cpu=platform.processor(), platform=platform.platform(),
                torch=torch.__version__, threads=torch.get_num_threads(),
                gpu=torch.cuda.get_device_name() if DEVICE.type == 'cuda' else None)


def split_fingerprints(splits):
    return {name: hashlib.sha256(frame.to_csv(index=False).encode('utf-8')).hexdigest()
            for name, frame in splits.items()}
