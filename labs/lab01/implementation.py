"""Minimal TF-IDF implementation for Lab 01.

The core implementation intentionally does not use sklearn's TfidfVectorizer.
It follows the formulas in the assignment:

    tf(t, d) = count(t, d) / total_terms(d)
    idf(t) = log(N / df(t))
    tfidf(t, d) = tf(t, d) * idf(t)
"""

from __future__ import annotations

from collections import Counter
from math import log, sqrt
from typing import Iterable, Sequence


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
