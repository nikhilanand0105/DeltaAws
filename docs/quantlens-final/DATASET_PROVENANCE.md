# QuantLens-XAI: Dataset Provenance, Preprocessing & Feature Engineering

**Course:** Explainable Artificial Intelligence (BCSE418L)  
**Academic Year:** 2026–27  
**Student:** Nikhil Anand

---

## 1. Raw Market Data Provenance

All historical financial time-series data utilized in QuantLens-XAI were acquired directly from Yahoo Finance via the official `yfinance` Python API, formatted into standard daily Open-High-Low-Close-Volume (OHLCV) records, and persisted as offline CSV files to ensure 100% offline academic reproducibility.

### Cached Assets Summary

| Symbol | Company / Index | Primary Exchange | Bar Resolution | Date Range | Total Daily Candles | Offline File Path |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **RELIANCE.NS** | Reliance Industries Ltd. | NSE (India) | Daily (1D) | 2020-01-01 to 2026-10-23 | 1,687 bars | `data/historical/RELIANCE.NS.csv` |
| **TCS.NS** | Tata Consultancy Services Ltd. | NSE (India) | Daily (1D) | 2020-01-01 to 2026-10-23 | 1,687 bars | `data/historical/TCS.NS.csv` |
| **INFY.NS** | Infosys Ltd. | NSE (India) | Daily (1D) | 2020-01-01 to 2026-10-23 | 1,687 bars | `data/historical/INFY.NS.csv` |
| **NIFTY50** | NIFTY 50 Benchmark Index | NSE (India) | Daily (1D) | 2020-01-01 to 2026-10-23 | 1,685 bars | `data/historical/NIFTY50.csv` |

---

## 2. Chronological Splitting (Zero Forward Leakage)

To satisfy the strict academic requirements of Slide 5 & 6, all datasets are split chronologically rather than with random shuffling. This guarantees zero future-data leakage across boundaries:

- **Training Set (70%)**: Bars 0 to 1,180 (2020-01-01 to 2024-09-15)
- **Validation Set (15%)**: Bars 1,181 to 1,433 (2024-09-16 to 2025-09-30)
- **Testing Set (15%)**: Bars 1,434 to 1,686 (2025-10-01 to 2026-10-23)

Feature scalers (`StandardScaler`) are fit exclusively on the training set and applied downstream to validation and testing sets.

---

## 3. 22 Causal Technical Indicators (Slides 6 & 7)

All features are calculated causally using historical information strictly prior to or at time $t$:

### 3.1 Trend Features
1. `sma_10`: 10-day Simple Moving Average
2. `sma_30`: 30-day Simple Moving Average
3. `sma_50`: 50-day Simple Moving Average
4. `ema_10`: 10-day Exponential Moving Average ($\alpha = 2/(10+1)$)
5. `ema_20`: 20-day Exponential Moving Average ($\alpha = 2/(20+1)$)
6. `ema_30`: 30-day Exponential Moving Average ($\alpha = 2/(30+1)$)
7. `ema_50`: 50-day Exponential Moving Average ($\alpha = 2/(50+1)$)

### 3.2 Momentum Features
8. `rsi_14`: Wilder's 14-day Relative Strength Index
9. `macd`: Fast EMA(12) - Slow EMA(26)
10. `macd_signal`: 9-day EMA of MACD
11. `macd_hist`: MACD - MACD Signal

### 3.3 Volatility Features
12. `bb_upper`: 20-day SMA + $2\sigma$
13. `bb_middle`: 20-day SMA
14. `bb_lower`: 20-day SMA - $2\sigma$
15. `bb_width`: $(\text{Upper} - \text{Lower}) / \text{Middle}$
16. `bb_pct_b`: $(\text{Close} - \text{Lower}) / (\text{Upper} - \text{Lower})$
17. `atr_14`: 14-day Average True Range

### 3.4 Volume Features
18. `vol_sma_ratio`: Volume / 20-day Volume SMA
19. `obv`: On-Balance Volume
20. `vol_pct_change`: Daily Volume % Change

### 3.5 Scale-Invariant Normalized Ratios
21. `price_to_sma10`: $(\text{Close} - \text{SMA}_{10}) / \text{SMA}_{10}$
22. `price_to_ema30`: $(\text{Close} - \text{EMA}_{30}) / \text{EMA}_{30}$

---

## 4. Classification Target Generation

The multi-class predictive target represents forward returns over a 5-bar horizon:
$$\text{Forward Return}_t = \frac{\text{Close}_{t+5} - \text{Close}_t}{\text{Close}_t}$$

$$\text{Target}_t = \begin{cases} 
2 \quad (\text{BUY}) & \text{if } \text{Forward Return}_t > +1.5\% \\
0 \quad (\text{SELL}) & \text{if } \text{Forward Return}_t < -1.5\% \\
1 \quad (\text{HOLD}) & \text{otherwise}
\end{cases}$$
