"""Monte Carlo risk analysis utilities.

This module provides a simple function to estimate Value at Risk (VaR)
using a geometric Brownian motion model.
"""

from __future__ import annotations

import math
import random
from typing import Tuple


def monte_carlo_var(
    initial_value: float = 10000.0,
    mu: float = 0.05,
    sigma: float = 0.2,
    horizon: float = 1.0,
    num_sims: int = 10000,
    alpha: float = 0.95,
    seed: int | None = None,
) -> Tuple[float, float]:
    """Estimate Value at Risk and Expected Shortfall with Monte Carlo.

    Args:
        initial_value: Starting portfolio value.
        mu: Expected return of the portfolio.
        sigma: Volatility of returns.
        horizon: Time horizon of the simulation in years.
        num_sims: Number of Monte Carlo simulations to run.
        alpha: Confidence level for the VaR/ES metrics.
        seed: Optional random seed for reproducibility.

    Returns:
        A tuple ``(var, expected_shortfall)`` expressed as positive losses.
    """
    if seed is not None:
        random.seed(seed)

    losses = []
    for _ in range(num_sims):
        z = random.gauss(0, 1)
        final_value = initial_value * math.exp(
            (mu - 0.5 * sigma ** 2) * horizon + sigma * math.sqrt(horizon) * z
        )
        loss = initial_value - final_value
        losses.append(loss)

    losses.sort()
    index = int(alpha * num_sims)
    var = losses[index]
    es = sum(losses[index:]) / (num_sims - index)
    return var, es


if __name__ == "__main__":
    var, es = monte_carlo_var()
    print(f"95% VaR: {var:,.2f}")
    print(f"95% Expected Shortfall: {es:,.2f}")
