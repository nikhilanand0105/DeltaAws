# QuantLens-XAI: Exact UI Navigation & Button Action Guide

**Course:** Explainable Artificial Intelligence (BCSE418L)  
**Academic Year:** 2026–27  
**Student:** Nikhil Anand  
**Target URL:** `http://127.0.0.1:5001/quantlens`

---

## 1. Top Global Navigation Header

| Element / Button | Visual Location | User Action | System Response |
| :--- | :--- | :--- | :--- |
| **Academic Warning Banner** | Top of screen (Purple/Indigo) | Read-only | Displays: `PAPER TRADING — VIRTUAL FUNDS ONLY • Academic Research Simulation Platform • BCSE418L` |
| **Brand Logo & Title** | Top Left | Clickable | Refreshes home view |
| **Ollama Status Pill** | Top Center | Read-only | Shows glowing green dot + `Ollama: qwen2.5:0.5b (Metal GPU)` |
| **Virtual Balance Chip** | Top Right | Read-only | Displays live portfolio equity: `Virtual Balance: ₹1,00,000.00` |
| **⚙️ Delta Bot Panel** | Top Far Right | Click | Navigates to `/dashboard` (Original cryptobot config panel) |

---

## 2. Tab Navigation & Interactive Panels

### Tab 1: 🧠 Strategy Builder (LLM)
- **`Preset 1: RELIANCE EMA 10/30 + RSI 65` (Chip)**:
  - *Click*: Pre-fills prompt textarea with the faculty demonstration strategy.
- **`Target Symbol` (Dropdown)**:
  - *Select*: `RELIANCE`, `TCS`, `INFY`, or `NIFTY50`.
- **`⚡ Compile with Local Ollama` (Purple Button)**:
  - *Click*: Displays loading spinner, calls local Ollama, populates the 7-step decision trace, AI risk advisory, and compiled JSON schema.
- **`Copy JSON` (Button)**:
  - *Click*: Copies compiled `StrategyDefinition` JSON to system clipboard.
- **`🚀 Accept & Run Historical Backtest` (Green Button)**:
  - *Click*: Automatically switches to Tab 2 and launches the deterministic backtest.

### Tab 2: 📈 Backtest & Analysis
- **`Cumulative Return`, `Sharpe Ratio`, `Max Drawdown`, `Win Rate` (KPI Tiles)**:
  - *Display*: Dynamic real-time calculated financial metrics.
- **`Candlestick Chart` (ApexCharts)**:
  - *Interact*: Zoom, pan, hover over candles to inspect OHLC, EMA 10, EMA 30, and BUY/SELL execution markers.
- **`RSI Indicator Panel`**:
  - *Interact*: Tracks 14-day RSI against the red 65 threshold line.
- **`Re-run Backtest` (Button)**:
  - *Click*: Re-executes the backtest algorithm.
- **`Backtest Execution Trades Log` (Table)**:
  - *Inspect*: Chronological list of all executed trades with entry/exit timestamps, prices, and net P&L.

### Tab 3: 🔬 ML & XAI Explainability
- **`XGBoost Classifier Card`**: Displays 78.4% test accuracy, 0.893 ROC-AUC, and TreeExplainer integration.
- **`PyTorch MLP Card`**: Displays 76.8% test accuracy, Apple Metal GPU acceleration, and 89.2% consensus agreement.
- **`Refresh XAI Attributions` (Button)**:
  - *Click*: Evaluates the latest historical bar through both models, refreshes SHAP waterfall bar chart and LIME rule weights.
- **`SHAP Feature Attribution Chart`**:
  - *Inspect*: Green bars (bullish positive push) vs. Red bars (bearish resistance).
- **`LIME Interpretable Rules Chart`**:
  - *Inspect*: Bounded interval decision rules with surrogate $R^2$ fidelity badge.
- **`Slide 9 Empirical Table`**:
  - *Inspect*: Full comparison across Fidelity, Stability, Consistency, Robustness, Sparsity, and Computational Cost.

### Tab 4: 💼 Paper Broker & Replay
- **`Virtual Portfolio Tiles`**: Displays Total Portfolio Value, Available Cash, Invested Value, and Unrealized P&L.
- **`▶️ Run Historical Replay` (Button)**:
  - *Click*: Replays recent 30, 60, or 120 bars, executes simulated paper orders, and updates cash balances.
- **`Place Virtual Paper Order` (Button)**:
  - *Click*: Places manual simulated order with slippage and fees.
- **`🔄 Reset Virtual Funds to ₹1,00,000` (Red Button)**:
  - *Click*: Clears all active virtual positions, orders, and restores virtual cash to ₹1,00,000.00 INR.
- **`Open Virtual Positions` (Table)**: Real-time mark-to-market positions.
- **`Paper Orders Ledger` (Table)**: Real-time orders (`ORD-XXXX`).
- **`Immutable Strategy-to-Order Audit Trail` (Table)**: Cryptographic trace (`AUD-XXXX`) linking strategy rules to order fills.
