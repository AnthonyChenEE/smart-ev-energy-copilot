# -*- coding: utf-8 -*-
"""data.py — Synthetic data generation for EV energy optimization

This module provides functions to generate realistic synthetic profiles
for home load, solar PV generation, and electricity pricing.
"""

import numpy as np
import pandas as pd


def synthetic_profiles(T: int = 24, seed: int = 42) -> pd.DataFrame:
    """
    Generate synthetic hourly profiles for home load, PV, and electricity prices.

    This function creates realistic test data for a 24-hour period including:
    - Home electrical load with daily patterns (higher in morning/evening)
    - Solar PV generation with Gaussian peak around noon
    - Time-of-use electricity pricing (off-peak, normal, peak)

    Parameters
    ----------
    T : int, default=24
        Number of time periods (hours)
    seed : int, default=42
        Random seed for reproducibility

    Returns
    -------
    pd.DataFrame
        DataFrame with columns:
        - 'hour': Hour index (0 to T-1)
        - 'load_kw': Home electrical load in kW
        - 'pv_kw': Solar PV generation in kW
        - 'price_buy': Grid purchase price in $/kWh

    Examples
    --------
    >>> df = synthetic_profiles(T=24)
    >>> df.head()
       hour   load_kw    pv_kw  price_buy
    0     0  0.826...  0.000...      0.18
    1     1  0.674...  0.000...      0.18
    """
    rng = np.random.default_rng(seed)
    hours = np.arange(T)

    # Home load: sinusoidal pattern with peak around 7pm, trough around 3am
    # Range: ~0.4 kW (night) to ~2.0 kW (evening)
    load = 1.2 + 0.8 * np.sin(2 * np.pi * (hours - 7) / 24)

    # Solar PV: Gaussian peak at noon (hour 12) with small random noise
    # Maximum ~5 kW at solar noon
    pv = np.maximum(
        5 * np.exp(-0.5 * ((hours - 12) / 3) ** 2) + rng.normal(0, 0.1, T),
        0  # Ensure non-negative
    )

    # Time-of-use electricity pricing ($/kWh)
    price = np.full(T, 0.30)  # Normal rate: $0.30/kWh
    price[(hours >= 22) | (hours < 7)] = 0.18  # Off-peak: $0.18/kWh (10pm-7am)
    price[(hours >= 17) & (hours <= 21)] = 0.48  # Peak: $0.48/kWh (5pm-9pm)

    return pd.DataFrame({
        'hour': hours,
        'load_kw': load,
        'pv_kw': pv,
        'price_buy': price
    })


def price_sell_vector(T: int = 24, feed_in_tariff: float = 0.08) -> np.ndarray:
    """
    Generate feed-in tariff (selling price) vector for grid export.

    Creates a constant feed-in tariff for all time periods. In real systems,
    this could vary by time of day or season.

    Parameters
    ----------
    T : int, default=24
        Number of time periods
    feed_in_tariff : float, default=0.08
        Feed-in tariff rate in $/kWh (price for selling excess energy to grid)

    Returns
    -------
    np.ndarray
        Array of length T with constant feed-in tariff values

    Examples
    --------
    >>> price_sell = price_sell_vector(T=24, feed_in_tariff=0.08)
    >>> price_sell.shape
    (24,)
    >>> price_sell[0]
    0.08
    """
    return np.full(T, feed_in_tariff)
