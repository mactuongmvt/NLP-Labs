"""Tiện ích tiền xử lý cho Lab 04."""

from __future__ import annotations

import re
from pathlib import Path

import numpy as np
import pandas as pd


TOKEN_PATTERN = re.compile(r"[A-Za-z]+(?:'[A-Za-z]+)?")


def load_imdb_splits(data_dir: str | Path) -> dict[str, pd.DataFrame]:
    """Đọc ba tập IMDb đã chia sẵn theo tỷ lệ 60/20/20."""
    data_dir = Path(data_dir)
    paths = {
        "train": data_dir / "imdb_train.csv.gz",
        "validation": data_dir / "imdb_validation.csv.gz",
        "test": data_dir / "imdb_test.csv.gz",
    }
    missing = [str(path) for path in paths.values() if not path.exists()]
    if missing:
        raise FileNotFoundError(f"Không tìm thấy dữ liệu: {missing}")
    return {name: pd.read_csv(path) for name, path in paths.items()}


def tokenize(text: str) -> list[str]:
    """Chuyển văn bản thành các token chữ thường dùng cho Word2Vec."""
    return TOKEN_PATTERN.findall(str(text).lower())


def average_word_vectors(
    tokenized_documents: list[list[str]],
    keyed_vectors,
) -> np.ndarray:
    """Lấy trung bình các vector đã có trong vocabulary cho từng document."""
    matrix = np.zeros(
        (len(tokenized_documents), keyed_vectors.vector_size), dtype=np.float32
    )
    for row_index, tokens in enumerate(tokenized_documents):
        vectors = [keyed_vectors[token] for token in tokens if token in keyed_vectors]
        if vectors:
            matrix[row_index] = np.mean(vectors, axis=0)
    return matrix
