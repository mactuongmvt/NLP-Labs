"""Simple RNN cell implemented from the recurrent equation."""

from __future__ import annotations

import torch
from torch import nn


class SimpleRNNCell(nn.Module):
    """Compute h_t = tanh(W_xh x_t + W_hh h_(t-1) + b_h)."""

    def __init__(self, input_size: int, hidden_size: int) -> None:
        super().__init__()
        self.input_size = input_size
        self.hidden_size = hidden_size
        self.W_xh = nn.Parameter(torch.empty(hidden_size, input_size))
        self.W_hh = nn.Parameter(torch.empty(hidden_size, hidden_size))
        self.b_h = nn.Parameter(torch.zeros(hidden_size))
        self.reset_parameters()

    def reset_parameters(self) -> None:
        nn.init.xavier_uniform_(self.W_xh)
        nn.init.orthogonal_(self.W_hh)
        nn.init.zeros_(self.b_h)

    def forward(self, x_t: torch.Tensor, h_prev: torch.Tensor) -> torch.Tensor:
        return torch.tanh(x_t @ self.W_xh.T + h_prev @ self.W_hh.T + self.b_h)
