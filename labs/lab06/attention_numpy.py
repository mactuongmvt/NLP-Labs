"""NumPy implementation of stable scaled dot-product attention."""

from __future__ import annotations

import numpy as np


def stable_softmax(scores: np.ndarray, axis: int = -1) -> np.ndarray:
    """Compute softmax after subtracting the maximum for numerical stability."""
    values = np.asarray(scores, dtype=np.float64)
    if values.size == 0:
        raise ValueError("scores must not be empty")
    if not np.all(np.isfinite(values)):
        raise ValueError("scores must contain only finite values")
    shifted = values - np.max(values, axis=axis, keepdims=True)
    exponentials = np.exp(shifted)
    return exponentials / np.sum(exponentials, axis=axis, keepdims=True)


def scaled_dot_product_attention(
    Q: np.ndarray,
    K: np.ndarray,
    V: np.ndarray,
    mask: np.ndarray | None = None,
    temperature: float = 1.0,
) -> tuple[np.ndarray, np.ndarray, np.ndarray]:
    """Return scaled scores, attention weights, and context.

    Q, K, and V may include leading batch dimensions. A True mask entry keeps
    a key; False entries receive zero attention weight.
    """
    query = np.asarray(Q, dtype=np.float64)
    keys = np.asarray(K, dtype=np.float64)
    values = np.asarray(V, dtype=np.float64)
    if query.ndim < 2 or keys.ndim < 2 or values.ndim < 2:
        raise ValueError("Q, K, and V must have at least two dimensions")
    if query.shape[-1] != keys.shape[-1]:
        raise ValueError("Q and K must have the same key dimension")
    if keys.shape[-2] != values.shape[-2]:
        raise ValueError("K and V must have the same sequence length")
    if not np.isfinite(temperature) or temperature <= 0:
        raise ValueError("temperature must be positive")
    if not all(np.all(np.isfinite(x)) for x in (query, keys, values)):
        raise ValueError("Q, K, and V must contain only finite values")

    scores = query @ np.swapaxes(keys, -1, -2)
    scores = scores / (np.sqrt(query.shape[-1]) * temperature)
    if mask is not None:
        keep = np.asarray(mask, dtype=bool)
        if keep.ndim == scores.ndim - 1 and keep.shape[-1] == scores.shape[-1]:
            keep = np.expand_dims(keep, axis=-2)
        try:
            keep = np.broadcast_to(keep, scores.shape)
        except ValueError as error:
            raise ValueError("mask is not broadcastable to the score shape") from error
        if np.any(~np.any(keep, axis=-1)):
            raise ValueError("each query must have at least one unmasked key")
        scores = np.where(keep, scores, -np.inf)
        row_max = np.max(scores, axis=-1, keepdims=True)
        exponentials = np.where(keep, np.exp(scores - row_max), 0.0)
        weights = exponentials / np.sum(exponentials, axis=-1, keepdims=True)
    else:
        weights = stable_softmax(scores, axis=-1)
    context = weights @ values
    return scores, weights, context


def self_attention(
    X: np.ndarray,
    WQ: np.ndarray,
    WK: np.ndarray,
    WV: np.ndarray,
    mask: np.ndarray | None = None,
) -> tuple[np.ndarray, np.ndarray, np.ndarray, np.ndarray]:
    """Project one sequence to Q/K/V and apply scaled self-attention."""
    inputs = np.asarray(X, dtype=np.float64)
    if inputs.ndim < 2 or inputs.shape[-1] != np.asarray(WQ).shape[0]:
        raise ValueError("X feature dimension must match the projection matrices")
    query = inputs @ np.asarray(WQ, dtype=np.float64)
    keys = inputs @ np.asarray(WK, dtype=np.float64)
    values = inputs @ np.asarray(WV, dtype=np.float64)
    scores, weights, context = scaled_dot_product_attention(query, keys, values, mask)
    return scores, weights, context, query
