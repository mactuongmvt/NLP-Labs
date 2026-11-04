"""Minimal post-norm Transformer encoder block using framework primitives."""

import math

import torch
from torch import nn


class MultiHeadSelfAttention(nn.Module):
    def __init__(self, d_model: int, n_heads: int, dropout: float = 0.1):
        super().__init__()
        if n_heads < 1 or d_model % n_heads:
            raise ValueError("d_model must be divisible by n_heads")
        self.n_heads = n_heads
        self.d_k = d_model // n_heads
        self.q_proj = nn.Linear(d_model, d_model)
        self.k_proj = nn.Linear(d_model, d_model)
        self.v_proj = nn.Linear(d_model, d_model)
        self.out_proj = nn.Linear(d_model, d_model)
        self.dropout = nn.Dropout(dropout)

    def forward(self, x, mask=None):
        batch, length, dimension = x.shape

        def split_heads(projection):
            return projection(x).reshape(batch, length, self.n_heads, self.d_k).transpose(1, 2)

        q, k, v = (split_heads(layer) for layer in (self.q_proj, self.k_proj, self.v_proj))
        scores = q @ k.transpose(-2, -1) / math.sqrt(self.d_k)
        if mask is not None:
            if mask.shape != (batch, length) or mask.dtype != torch.bool:
                raise ValueError("mask must be Boolean with shape (batch, time)")
            if not mask.any(dim=1).all():
                raise ValueError("Every sequence needs at least one valid token")
            scores = scores.masked_fill(~mask[:, None, None, :], float("-inf"))
        weights = torch.softmax(scores, dim=-1)
        attended = self.dropout(weights) @ v
        merged = attended.transpose(1, 2).contiguous().reshape(batch, length, dimension)
        return self.out_proj(merged), weights


class TransformerBlock(nn.Module):
    def __init__(self, d_model: int, n_heads: int, d_ff: int, dropout: float = 0.1):
        super().__init__()
        self.attention = MultiHeadSelfAttention(d_model, n_heads, dropout)
        self.norm1 = nn.LayerNorm(d_model)
        self.norm2 = nn.LayerNorm(d_model)
        self.ffn = nn.Sequential(
            nn.Linear(d_model, d_ff),
            nn.ReLU(),
            nn.Dropout(dropout),
            nn.Linear(d_ff, d_model),
        )
        self.dropout1 = nn.Dropout(dropout)
        self.dropout2 = nn.Dropout(dropout)

    def forward(self, x, mask=None, return_attention=False):
        attended, weights = self.attention(x, mask)
        hidden = self.norm1(x + self.dropout1(attended))
        output = self.norm2(hidden + self.dropout2(self.ffn(hidden)))
        if mask is not None:
            output = output * mask.unsqueeze(-1)
        return (output, weights) if return_attention else output
