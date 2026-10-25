"""
Feature Engineering Engine for QuantLens-XAI.
Computes all PPT Slide 6 & 7 technical indicators causally from daily OHLCV bars:
- Trend: SMA(10, 30, 50), EMA(10, 20, 30, 50)
- Momentum: RSI(14), MACD(12, 26, 9)
- Volatility: Bollinger Bands(20, 2), ATR(14)
- Volume: Volume SMA ratio, OBV, Volume Change %
Guarantees zero future-data leakage.
"""

import pandas as pd
import numpy as np
from typing import Tuple, List, Optional


FEATURE_COLUMNS = [
    "sma_10", "sma_30", "sma_50",
    "ema_10", "ema_20", "ema_30", "ema_50",
    "rsi_14",
    "macd", "macd_signal", "macd_hist",
    "bb_upper", "bb_middle", "bb_lower", "bb_width", "bb_pct_b",
    "atr_14",
    "vol_sma_ratio", "obv", "vol_pct_change",
    "price_to_sma10", "price_to_ema30"
]


def calculate_rsi(series: pd.Series, period: int = 14) -> pd.Series:
    """Calculates Wilder's Relative Strength Index (RSI)."""
    delta = series.diff()
    gain = delta.clip(lower=0)
    loss = -delta.clip(upper=0)

    # Exponential moving average with alpha = 1 / period (Wilder's smoothing)
    avg_gain = gain.ewm(alpha=1.0 / period, min_periods=period, adjust=False).mean()
    avg_loss = loss.ewm(alpha=1.0 / period, min_periods=period, adjust=False).mean()

    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi = 100.0 - (100.0 / (1.0 + rs))
    return rsi.fillna(50.0)


def calculate_macd(
    series: pd.Series,
    fast_period: int = 12,
    slow_period: int = 26,
    signal_period: int = 9
) -> Tuple[pd.Series, pd.Series, pd.Series]:
    """Calculates MACD line, Signal line, and MACD Histogram."""
    fast_ema = series.ewm(span=fast_period, adjust=False).mean()
    slow_ema = series.ewm(span=slow_period, adjust=False).mean()
    macd_line = fast_ema - slow_ema
    signal_line = macd_line.ewm(span=signal_period, adjust=False).mean()
    macd_hist = macd_line - signal_line
    return macd_line, signal_line, macd_hist


def calculate_bollinger_bands(
    series: pd.Series,
    period: int = 20,
    num_std: float = 2.0
) -> Tuple[pd.Series, pd.Series, pd.Series, pd.Series, pd.Series]:
    """Calculates Bollinger Bands: Middle, Upper, Lower, Bandwidth, and %B."""
    middle = series.rolling(window=period).mean()
    std = series.rolling(window=period).std()
    upper = middle + (std * num_std)
    lower = middle - (std * num_std)
    width = (upper - lower) / middle.replace(0, np.nan)
    pct_b = (series - lower) / (upper - lower).replace(0, np.nan)
    return upper, middle, lower, width.fillna(0), pct_b.fillna(0.5)


def calculate_atr(df: pd.DataFrame, period: int = 14) -> pd.Series:
    """Calculates Wilder's Average True Range (ATR)."""
    high = df["high"]
    low = df["low"]
    prev_close = df["close"].shift(1)

    tr1 = high - low
    tr2 = (high - prev_close).abs()
    tr3 = (low - prev_close).abs()
    true_range = pd.concat([tr1, tr2, tr3], axis=1).max(axis=1)

    atr = true_range.ewm(alpha=1.0 / period, min_periods=period, adjust=False).mean()
    return atr.bfill()


def calculate_obv(df: pd.DataFrame) -> pd.Series:
    """Calculates On-Balance Volume (OBV)."""
    close_diff = df["close"].diff()
    direction = np.where(close_diff > 0, 1, np.where(close_diff < 0, -1, 0))
    obv = (df["volume"] * direction).cumsum()
    return pd.Series(obv, index=df.index, name="obv")


def extract_technical_features(df: pd.DataFrame) -> pd.DataFrame:
    """
    Computes all PPT technical indicators on the given OHLCV DataFrame.
    Returns a new DataFrame containing all engineered causal features.
    """
    data = df.copy()

    # Trend Indicators
    data["sma_10"] = data["close"].rolling(10).mean()
    data["sma_30"] = data["close"].rolling(30).mean()
    data["sma_50"] = data["close"].rolling(50).mean()

    data["ema_10"] = data["close"].ewm(span=10, adjust=False).mean()
    data["ema_20"] = data["close"].ewm(span=20, adjust=False).mean()
    data["ema_30"] = data["close"].ewm(span=30, adjust=False).mean()
    data["ema_50"] = data["close"].ewm(span=50, adjust=False).mean()

    # Momentum Indicators
    data["rsi_14"] = calculate_rsi(data["close"], period=14)
    macd, macd_sig, macd_hist = calculate_macd(data["close"])
    data["macd"] = macd
    data["macd_signal"] = macd_sig
    data["macd_hist"] = macd_hist

    # Volatility Indicators
    bb_u, bb_m, bb_l, bb_w, bb_b = calculate_bollinger_bands(data["close"])
    data["bb_upper"] = bb_u
    data["bb_middle"] = bb_m
    data["bb_lower"] = bb_l
    data["bb_width"] = bb_w
    data["bb_pct_b"] = bb_b
    data["atr_14"] = calculate_atr(data, period=14)

    # Volume Indicators
    vol_sma20 = data["volume"].rolling(20).mean().replace(0, np.nan)
    data["vol_sma_ratio"] = (data["volume"] / vol_sma20).fillna(1.0)
    data["obv"] = calculate_obv(data)
    data["vol_pct_change"] = data["volume"].pct_change().fillna(0.0)

    # Relative Ratios (scale-invariant normalized features)
    data["price_to_sma10"] = (data["close"] - data["sma_10"]) / data["sma_10"].replace(0, np.nan)
    data["price_to_ema30"] = (data["close"] - data["ema_30"]) / data["ema_30"].replace(0, np.nan)

    return data


def generate_ml_dataset(
    df: pd.DataFrame,
    forecast_horizon: int = 5,
    threshold_pct: float = 0.015
) -> Tuple[pd.DataFrame, pd.Series, List[str]]:
    """
    Generates feature matrix X and classification target y for BUY/HOLD/SELL.
    Target labels:
      0 = SELL (forward return < -threshold_pct)
      1 = HOLD (-threshold_pct <= forward return <= threshold_pct)
      2 = BUY  (forward return > threshold_pct)
    """
    data = extract_technical_features(df)

    # Future return over forecast_horizon bars
    future_close = data["close"].shift(-forecast_horizon)
    forward_return = (future_close - data["close"]) / data["close"]

    # Target class
    target = pd.Series(1, index=data.index, name="target")  # default HOLD
    target = np.where(forward_return > threshold_pct, 2, np.where(forward_return < -threshold_pct, 0, 1))
    target = pd.Series(target, index=data.index, name="target")

    # Drop warm-up bars (first 50 bars where indicators are forming) and last forecast_horizon bars
    valid_idx = slice(50, len(data) - forecast_horizon)
    X = data.iloc[valid_idx][FEATURE_COLUMNS].copy()
    y = target.iloc[valid_idx].copy()

    # Fill any residual NaNs/Infs with forward/backward fill then 0
    X = X.replace([np.inf, -np.inf], np.nan).ffill().bfill().fillna(0.0)

    return X, y, FEATURE_COLUMNS
