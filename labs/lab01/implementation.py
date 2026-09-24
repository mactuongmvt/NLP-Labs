"""Minimal TF-IDF implementation for Lab 01.

The core implementation intentionally does not use sklearn's TfidfVectorizer.
It follows the formulas in the assignment:

    tf(t, d) = count(t, d) / total_terms(d)
    idf(t) = log(N / df(t))
    tfidf(t, d) = tf(t, d) * idf(t)
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
import gzip
import json
from math import log, sqrt
from pathlib import Path
import re
from typing import Callable, Iterable, Sequence
import unicodedata

import numpy as np
import pandas as pd
from scipy import sparse
from sklearn.feature_extraction.text import CountVectorizer, ENGLISH_STOP_WORDS
from sklearn.preprocessing import normalize
from tokenizers import Tokenizer
from tokenizers.models import BPE
from tokenizers.pre_tokenizers import Whitespace
from tokenizers.trainers import BpeTrainer


def _tokenize(document: str) -> list[str]:
    """Apply the minimal Lab 01 tokenization convention."""
    return document.lower().split()


def build_vocabulary(documents: Sequence[str]) -> dict[str, int]:
    """Build a deterministic, alphabetically ordered term-to-index mapping."""
    terms = {token for document in documents for token in _tokenize(document)}
    return {term: index for index, term in enumerate(sorted(terms))}


def compute_counts(document: str, vocabulary: dict[str, int]) -> list[int]:
    """Return the count vector of one document using a fixed vocabulary."""
    token_counts = Counter(_tokenize(document))
    counts = [0] * len(vocabulary)
    for term, index in vocabulary.items():
        counts[index] = token_counts.get(term, 0)
    return counts


def compute_tf(counts: Sequence[int]) -> list[float]:
    """Normalize a count vector by the total number of in-vocabulary terms."""
    total = sum(counts)
    if total == 0:
        return [0.0] * len(counts)
    return [count / total for count in counts]


def compute_idf(count_matrix: Sequence[Sequence[int]]) -> list[float]:
    """Compute unsmoothed IDF values: log(N / df)."""
    number_of_documents = len(count_matrix)
    if number_of_documents == 0:
        return []

    vocabulary_size = len(count_matrix[0])
    if any(len(row) != vocabulary_size for row in count_matrix):
        raise ValueError("All count vectors must have the same length")

    document_frequencies = [
        sum(1 for row in count_matrix if row[index] > 0)
        for index in range(vocabulary_size)
    ]
    if any(df == 0 for df in document_frequencies):
        raise ValueError("Every vocabulary term must occur in at least one document")

    return [log(number_of_documents / df) for df in document_frequencies]


def compute_tfidf(
    term_frequencies: Sequence[float], idf_values: Sequence[float]
) -> list[float]:
    """Multiply corresponding TF and IDF components."""
    if len(term_frequencies) != len(idf_values):
        raise ValueError("TF and IDF vectors must have the same length")
    return [tf * idf for tf, idf in zip(term_frequencies, idf_values)]


def cosine_similarity(vector_x: Iterable[float], vector_y: Iterable[float]) -> float:
    """Compute cosine similarity, returning 0.0 if either vector is zero."""
    x = list(vector_x)
    y = list(vector_y)
    if len(x) != len(y):
        raise ValueError("Vectors must have the same length")

    dot_product = sum(a * b for a, b in zip(x, y))
    norm_x = sqrt(sum(value * value for value in x))
    norm_y = sqrt(sum(value * value for value in y))
    if norm_x == 0.0 or norm_y == 0.0:
        return 0.0
    return dot_product / (norm_x * norm_y)


# The helpers below support the 30K-document experiments in experiments.ipynb.
Tokenize = Callable[[str], list[str]]


@dataclass
class Representation:
    name: str
    vectorizer: CountVectorizer
    counts: sparse.csr_matrix
    tfidf: sparse.csr_matrix
    normalized_tfidf: sparse.csr_matrix
    document_frequency: np.ndarray
    idf: np.ndarray
    average_tokens: float
    sparsity: float


def load_c4_documents(path: str | Path) -> pd.DataFrame:
    """Load the gzipped JSON Lines C4 sample."""
    records: list[dict[str, object]] = []
    with gzip.open(path, "rt", encoding="utf-8") as stream:
        for document_id, line in enumerate(stream):
            item = json.loads(line)
            records.append(
                {
                    "document_id": document_id,
                    "text": item["text"],
                    "url": item.get("url", ""),
                    "timestamp": item.get("timestamp", ""),
                }
            )
    return pd.DataFrame.from_records(records)


def minimal_tokenize(text: str) -> list[str]:
    """Pipeline A: lowercase followed by whitespace tokenization."""
    return text.lower().split()


_NORMALIZED_TOKEN_PATTERN = re.compile(r"[a-z0-9]+(?:'[a-z0-9]+)?")


def normalized_tokenize(text: str) -> list[str]:
    """Pipeline B: lowercase, punctuation normalization, and stopword removal."""
    text = unicodedata.normalize("NFKC", text).lower()
    return [
        token
        for token in _NORMALIZED_TOKEN_PATTERN.findall(text)
        if token not in ENGLISH_STOP_WORDS
    ]


def train_subword_tokenizer(
    documents: Sequence[str], vocabulary_size: int = 30_000
) -> Tokenizer:
    """Train the BPE tokenizer used by Pipeline C."""
    tokenizer = Tokenizer(BPE(unk_token="[UNK]"))
    tokenizer.pre_tokenizer = Whitespace()
    trainer = BpeTrainer(
        vocab_size=vocabulary_size,
        min_frequency=2,
        special_tokens=["[UNK]"],
    )
    tokenizer.train_from_iterator(
        (unicodedata.normalize("NFKC", document).lower() for document in documents),
        trainer=trainer,
        length=len(documents),
    )
    return tokenizer


def make_subword_tokenize(tokenizer: Tokenizer) -> Tokenize:
    """Adapt a trained Hugging Face tokenizer to CountVectorizer's API."""
    return lambda text: tokenizer.encode(
        unicodedata.normalize("NFKC", text).lower()
    ).tokens


def heldout_oov_rate(
    training_documents: Sequence[str],
    heldout_documents: Sequence[str],
    tokenize: Tokenize,
    known_vocabulary: set[str] | None = None,
) -> float:
    """Measure token OOV rate on documents excluded from vocabulary construction."""
    if known_vocabulary is None:
        known_vocabulary = {
            token for document in training_documents for token in tokenize(document)
        }

    total = 0
    out_of_vocabulary = 0
    for document in heldout_documents:
        for token in tokenize(document):
            total += 1
            if token == "[UNK]" or token not in known_vocabulary:
                out_of_vocabulary += 1
    return out_of_vocabulary / total if total else 0.0


def build_representation(
    documents: Sequence[str], name: str, tokenize: Tokenize
) -> Representation:
    """Build count, TF, IDF, and sparse TF-IDF representations."""
    vectorizer = CountVectorizer(
        tokenizer=tokenize,
        token_pattern=None,
        lowercase=False,
        dtype=np.float64,
    )
    counts = vectorizer.fit_transform(documents).tocsr()
    number_of_documents, vocabulary_size = counts.shape

    row_totals = np.asarray(counts.sum(axis=1)).ravel()
    safe_row_totals = np.where(row_totals == 0, 1.0, row_totals)
    term_frequency = sparse.diags(1.0 / safe_row_totals) @ counts

    document_frequency = np.asarray(counts.getnnz(axis=0)).ravel()
    idf = np.log(number_of_documents / document_frequency)
    tfidf = term_frequency.multiply(idf).tocsr()
    normalized_tfidf = normalize(tfidf, norm="l2", axis=1).tocsr()
    sparsity = 1.0 - counts.nnz / (number_of_documents * vocabulary_size)

    return Representation(
        name=name,
        vectorizer=vectorizer,
        counts=counts,
        tfidf=tfidf,
        normalized_tfidf=normalized_tfidf,
        document_frequency=document_frequency,
        idf=idf,
        average_tokens=float(row_totals.mean()),
        sparsity=float(sparsity),
    )


def representation_summary(model: Representation) -> dict[str, object]:
    """Return the main quantitative properties of a representation."""
    number_of_documents, vocabulary_size = model.counts.shape
    return {
        "pipeline": model.name,
        "documents": number_of_documents,
        "vocabulary_size": vocabulary_size,
        "average_tokens_per_document": model.average_tokens,
        "nonzero_entries": model.counts.nnz,
        "sparsity": model.sparsity,
    }


def inspect_terms(
    model: Representation, document_id: int = 0, number_of_terms: int = 20
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Inspect top terms by DF, IDF, and TF-IDF in one document."""
    terms = model.vectorizer.get_feature_names_out()
    top_df_indices = np.argsort(model.document_frequency)[-number_of_terms:][::-1]
    top_idf_indices = np.argsort(model.idf)[-number_of_terms:][::-1]

    row = model.tfidf.getrow(document_id)
    row_order = np.argsort(row.data)[-number_of_terms:][::-1]
    top_tfidf_indices = row.indices[row_order]

    top_df = pd.DataFrame(
        {
            "term": terms[top_df_indices],
            "document_frequency": model.document_frequency[top_df_indices],
        }
    )
    top_idf = pd.DataFrame(
        {"term": terms[top_idf_indices], "idf": model.idf[top_idf_indices]}
    )
    top_tfidf = pd.DataFrame(
        {"term": terms[top_tfidf_indices], "tfidf": row.data[row_order]}
    )
    return top_df, top_idf, top_tfidf


def query_oov_rate(model: Representation, queries: Sequence[str]) -> float:
    """Compute OOV rate over the fixed evaluation-query token stream."""
    analyzer = model.vectorizer.build_analyzer()
    vocabulary = model.vectorizer.vocabulary_
    tokens = [token for query in queries for token in analyzer(query)]
    if not tokens:
        return 0.0
    return sum(token not in vocabulary for token in tokens) / len(tokens)


def search(
    query: str,
    model: Representation,
    documents: pd.DataFrame,
    top_k: int = 5,
) -> pd.DataFrame:
    """Rank documents by cosine similarity to a TF-IDF query vector."""
    query_counts = model.vectorizer.transform([query]).tocsr()
    total = float(query_counts.sum())
    if total == 0.0:
        return pd.DataFrame(
            columns=["rank", "document_id", "similarity", "document_preview"]
        )

    query_tf = query_counts / total
    query_tfidf = query_tf.multiply(model.idf).tocsr()
    query_vector = normalize(query_tfidf, norm="l2", axis=1).tocsr()
    scores = (model.normalized_tfidf @ query_vector.T).toarray().ravel()
    candidate_indices = np.argpartition(scores, -top_k)[-top_k:]
    ranked_indices = candidate_indices[np.argsort(scores[candidate_indices])[::-1]]

    rows = []
    for rank, document_id in enumerate(ranked_indices, start=1):
        preview = " ".join(documents.iloc[document_id]["text"].split())[:240]
        rows.append(
            {
                "rank": rank,
                "document_id": int(document_id),
                "similarity": float(scores[document_id]),
                "document_preview": preview,
            }
        )
    return pd.DataFrame(rows)


def explain_similarity_contributions(
    query: str,
    document_id: int,
    model: Representation,
    max_terms: int = 5,
) -> pd.DataFrame:
    """Explain cosine similarity using nonzero normalized TF-IDF term products."""
    columns = ["term", "query_weight", "document_weight", "contribution"]
    if max_terms <= 0:
        return pd.DataFrame(columns=columns)
    if document_id < 0 or document_id >= model.normalized_tfidf.shape[0]:
        raise IndexError(f"document_id out of range: {document_id}")

    query_counts = model.vectorizer.transform([query]).tocsr()
    total = float(query_counts.sum())
    if total == 0.0:
        return pd.DataFrame(columns=columns)

    query_tf = query_counts / total
    query_tfidf = query_tf.multiply(model.idf).tocsr()
    query_vector = normalize(query_tfidf, norm="l2", axis=1).tocsr()
    document_vector = model.normalized_tfidf.getrow(document_id)
    contributions = query_vector.multiply(document_vector).tocsr()
    if contributions.nnz == 0:
        return pd.DataFrame(columns=columns)

    terms = model.vectorizer.get_feature_names_out()
    order = np.argsort(contributions.data)[::-1][:max_terms]
    term_indices = contributions.indices[order]
    query_weights = np.asarray(query_vector[:, term_indices].toarray()).ravel()
    document_weights = np.asarray(document_vector[:, term_indices].toarray()).ravel()
    return pd.DataFrame(
        {
            "term": terms[term_indices],
            "query_weight": query_weights,
            "document_weight": document_weights,
            "contribution": contributions.data[order],
        }
    )


def retrieval_metrics(
    retrieved_ids: Sequence[int], relevant_ids: set[int], k: int = 5
) -> dict[str, float]:
    """Compute Precision@K, Recall@K, and reciprocal rank for one query."""
    top_k = list(retrieved_ids[:k])
    hits = [document_id in relevant_ids for document_id in top_k]
    precision = sum(hits) / k
    recall = sum(hits) / len(relevant_ids) if relevant_ids else 0.0
    reciprocal_rank = next(
        (1.0 / rank for rank, hit in enumerate(hits, start=1) if hit), 0.0
    )
    return {
        f"precision@{k}": precision,
        f"recall@{k}": recall,
        "reciprocal_rank": reciprocal_rank,
    }
