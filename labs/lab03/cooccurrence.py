"""Core co-occurrence representation used in Lab 03."""

from __future__ import annotations

from collections import Counter
import gzip
import json
import re
import unicodedata
from pathlib import Path
from typing import Iterable, Sequence

import numpy as np
from scipy.sparse import csr_matrix, issparse


TOKEN_PATTERN = re.compile(r"[a-z]+(?:'[a-z]+)?|\d+(?:[.,]\d+)?")
SENTENCE_BOUNDARY = re.compile(r"(?:[.!?]+\s+|\n+)")


def tokenize(text: str) -> list[str]:
    """Normalize and tokenize English text."""
    normalized = unicodedata.normalize("NFKC", text).lower()
    normalized = normalized.replace("’", "'").replace("‘", "'")
    return TOKEN_PATTERN.findall(normalized)


def load_c4_documents(path: str | Path, limit: int | None = None) -> list[str]:
    """Load the text field from a gzipped C4 JSON Lines file."""
    documents: list[str] = []
    with gzip.open(Path(path), "rt", encoding="utf-8") as stream:
        for line in stream:
            record = json.loads(line)
            text = record.get("text", "")
            if text:
                documents.append(text)
            if limit is not None and len(documents) >= limit:
                break
    return documents


def prepare_sentences(
    documents: Iterable[str], max_sentence_length: int = 80
) -> list[list[str]]:
    """Split documents into tokenized sentences and cap long web-text spans."""
    sentences: list[list[str]] = []
    for document in documents:
        for span in SENTENCE_BOUNDARY.split(document):
            tokens = tokenize(span)
            for start in range(0, len(tokens), max_sentence_length):
                chunk = tokens[start : start + max_sentence_length]
                if len(chunk) >= 2:
                    sentences.append(chunk)
    return sentences


def build_vocabulary(
    corpus: Iterable[Sequence[str]],
    min_count: int = 1,
    max_size: int | None = None,
) -> dict[str, int]:
    """Build a deterministic word-to-index mapping from tokenized sentences."""
    counts = Counter(token for sentence in corpus for token in sentence)
    words = [word for word, count in counts.items() if count >= min_count]
    words.sort(key=lambda word: (-counts[word], word))
    if max_size is not None:
        words = words[:max_size]
    return {word: index for index, word in enumerate(words)}


def build_cooccurrence_matrix(
    corpus: Iterable[Sequence[str]],
    vocabulary: dict[str, int],
    window_size: int = 1,
) -> csr_matrix:
    """Count target-context pairs within a symmetric context window."""
    if window_size < 1:
        raise ValueError("window_size must be at least 1")

    pair_counts: Counter[tuple[int, int]] = Counter()
    for sentence in corpus:
        indices = [vocabulary.get(token) for token in sentence]
        for position, target_index in enumerate(indices):
            if target_index is None:
                continue
            left = max(0, position - window_size)
            right = min(len(indices), position + window_size + 1)
            for context_position in range(left, right):
                if context_position == position:
                    continue
                context_index = indices[context_position]
                if context_index is not None:
                    pair_counts[(target_index, context_index)] += 1

    if not pair_counts:
        size = len(vocabulary)
        return csr_matrix((size, size), dtype=np.float64)

    rows, columns, values = zip(
        *((row, column, value) for (row, column), value in pair_counts.items())
    )
    size = len(vocabulary)
    return csr_matrix(
        (np.asarray(values, dtype=np.float64), (rows, columns)),
        shape=(size, size),
    )


def cosine_similarity(vector_a, vector_b) -> float:
    """Compute cosine similarity for dense or sparse vectors."""
    if issparse(vector_a):
        vector_a = vector_a.toarray().ravel()
    else:
        vector_a = np.asarray(vector_a, dtype=np.float64).ravel()
    if issparse(vector_b):
        vector_b = vector_b.toarray().ravel()
    else:
        vector_b = np.asarray(vector_b, dtype=np.float64).ravel()

    denominator = np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
    if denominator == 0:
        return 0.0
    return float(np.dot(vector_a, vector_b) / denominator)


def most_similar(
    word: str,
    matrix,
    vocabulary: dict[str, int],
    top_k: int = 5,
) -> list[tuple[str, float]]:
    """Return the nearest rows to a word vector by cosine similarity."""
    if word not in vocabulary:
        raise KeyError(f"Word not in vocabulary: {word}")
    if top_k < 1:
        return []

    index_to_word = {index: token for token, index in vocabulary.items()}
    target_index = vocabulary[word]

    if issparse(matrix):
        target = matrix.getrow(target_index)
        target_norm = np.sqrt(target.multiply(target).sum())
        row_norms = np.sqrt(matrix.multiply(matrix).sum(axis=1)).A1
        dots = (matrix @ target.T).toarray().ravel()
    else:
        dense = np.asarray(matrix, dtype=np.float64)
        target = dense[target_index]
        target_norm = np.linalg.norm(target)
        row_norms = np.linalg.norm(dense, axis=1)
        dots = dense @ target

    denominators = row_norms * target_norm
    scores = np.divide(
        dots,
        denominators,
        out=np.zeros_like(dots, dtype=np.float64),
        where=denominators != 0,
    )
    scores[target_index] = -np.inf
    best_indices = np.argsort(-scores, kind="stable")[:top_k]
    return [(index_to_word[index], float(scores[index])) for index in best_indices]


def word_similarity(
    word_a: str,
    word_b: str,
    matrix,
    vocabulary: dict[str, int],
) -> float:
    """Compute similarity between two words represented by matrix rows."""
    if word_a not in vocabulary or word_b not in vocabulary:
        return float("nan")
    return cosine_similarity(
        matrix[vocabulary[word_a]], matrix[vocabulary[word_b]]
    )
