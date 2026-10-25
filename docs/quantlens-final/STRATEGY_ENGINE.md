# QuantLens-XAI: Quantitative Strategy Engine

## 1. Overview
The Strategy Engine translates validated strategy schemas into executable algorithmic trading signals evaluated bar-by-bar across historical or live market feeds.

---

## 2. Supported Technical Indicators
- **Exponential Moving Average (EMA)**:
  $$\text{EMA}_t = \alpha \cdot P_t + (1 - \alpha) \cdot \text{EMA}_{t-1}, \quad \alpha = \frac{2}{N + 1}$$
- **Relative Strength Index (RSI)**:
  $$\text{RSI} = 100 - \frac{100}{1 + \text{RS}}, \quad \text{RS} = \frac{\text{Average Gain}}{\text{Average Loss}}$$
- **Moving Average Convergence Divergence (MACD)**:
  $$\text{MACD Line} = \text{EMA}_{12} - \text{EMA}_{26}, \quad \text{Signal Line} = \text{EMA}_9(\text{MACD})$$
- **Average True Range (ATR)**: Volatility measurement across $N=14$ bars.

---

## 3. Signal Generation & Risk Constraints
Signals evaluate:
1. **Entry Triggers**: Bullish crossover ($\text{EMA}_{\text{fast}} > \text{EMA}_{\text{slow}}$) AND indicator filter ($\text{RSI} < \theta_{\text{max}}$).
2. **Exit Triggers**: Bearish crossover or breach of stop-loss / take-profit percentage boundaries.
3. **Position Sizing**: Dynamically constrained by `max_capital_allocation_pct` and available cash in the paper broker account.
