"""Sinusoidal positional encoding for batch-first sequence tensors."""

import math

import torch
from torch import nn


def sinusoidal_encoding(max_length: int, d_model: int) -> torch.Tensor:
    if max_length < 1 or d_model < 1:
        raise ValueError("max_length and d_model must be positive")
    positions = torch.arange(max_length, dtype=torch.float32).unsqueeze(1)
    frequencies = torch.exp(
        torch.arange(0, d_model, 2, dtype=torch.float32)
        * (-math.log(10000.0) / d_model)
    )
    angles = positions * frequencies
    encoding = torch.zeros(max_length, d_model)
    encoding[:, 0::2] = torch.sin(angles)
    encoding[:, 1::2] = torch.cos(angles[:, : d_model // 2])
    return encoding


class PositionalEncoding(nn.Module):
    def __init__(self, d_model: int, max_length: int = 1024):
        super().__init__()
        self.register_buffer("encoding", sinusoidal_encoding(max_length, d_model))

    def forward(self, x: torch.Tensor) -> torch.Tensor:
        if x.ndim != 3 or x.shape[-1] != self.encoding.shape[-1]:
            raise ValueError("Expected x with shape (batch, time, d_model)")
        if x.shape[1] > self.encoding.shape[0]:
            raise ValueError("Sequence exceeds positional encoding capacity")
        return x + self.encoding[: x.shape[1]].to(dtype=x.dtype).unsqueeze(0)
