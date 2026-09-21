from math import isclose, log, sqrt

import pytest

from labs.lab01.implementation import (
    build_vocabulary,
    compute_counts,
    compute_idf,
    compute_tf,
    compute_tfidf,
    cosine_similarity,
)


CORPUS = ["cat eats fish", "dog eats fish", "cat likes fish"]
VOCABULARY = {"cat": 0, "dog": 1, "eats": 2, "fish": 3, "likes": 4}


def test_build_vocabulary_is_alphabetical_and_deterministic():
    assert build_vocabulary(CORPUS) == VOCABULARY


def test_compute_counts():
    assert compute_counts(CORPUS[0], VOCABULARY) == [1, 0, 1, 1, 0]


def test_compute_tf_sums_to_one():
    tf = compute_tf([1, 0, 1, 1, 0])
    assert isclose(sum(tf), 1.0)
    assert isclose(tf[0], 1 / 3)


def test_compute_tf_of_empty_document_is_zero_vector():
    assert compute_tf([0, 0, 0]) == [0.0, 0.0, 0.0]


def test_compute_idf_uses_unsmoothed_assignment_formula():
    matrix = [compute_counts(document, VOCABULARY) for document in CORPUS]
    actual = compute_idf(matrix)
    expected = [log(3 / 2), log(3), log(3 / 2), log(1), log(3)]
    assert actual == pytest.approx(expected)


def test_compute_tfidf():
    tf = [1 / 3, 0.0, 1 / 3, 1 / 3, 0.0]
    idf = [log(3 / 2), log(3), log(3 / 2), log(1), log(3)]
    assert compute_tfidf(tf, idf) == pytest.approx(
        [log(3 / 2) / 3, 0.0, log(3 / 2) / 3, 0.0, 0.0]
    )


def test_cosine_similarity():
    assert cosine_similarity([1, 1, 1], [1, 1, 0]) == pytest.approx(2 / sqrt(6))


def test_cosine_similarity_with_zero_vector():
    assert cosine_similarity([0, 0], [1, 1]) == 0.0
