# QuantLens-XAI: Academic Demo & Faculty Presentation Guide

## 1. Demo Objectives
Deliver an impressive, seamless 10-minute faculty walkthrough for BCSE418L demonstrating real quantitative modeling, local LLM parsing, hybrid databases, and explainable AI.

---

## 2. Seven-Step Demo Walkthrough

### Step 1: System Status & Hybrid Database (1 minute)
- Point out the **🍃 Hybrid DB: SQLite + MongoDB** badge in the header.
- Explain: SQLite preserves the legacy bot configuration, while MongoDB Community 7.0 manages real-time paper trading orders, positions, and XAI caches.
- Open `/api/quantlens/db-status` in a browser tab to demonstrate active connection counts for both databases.

### Step 2: Natural Language Strategy Parsing (2 minutes)
- In the **Strategy Builder** tab, click **Preset 1 (RELIANCE EMA 10/30 + RSI 65)**.
- Click **Parse & Generate Strategy**.
- Show:
  - Latency badge ($\approx 1,000\text{ ms}$ via local `qwen2.5:0.5b`).
  - Seven-Stage Visual Decision Trace highlighting tokenization, schema validation, and risk checks.
  - AI Risk Advisory card with confidence score (88%) and risk tier (MODERATE).
  - Validated Pydantic v2 JSON schema.

### Step 3: Event-Driven Backtesting (2 minutes)
- Click **Proceed to Backtest** (or **Backtest Engine** tab).
- Click **Run Backtest**.
- Show:
  - Dynamic Candlestick chart with overlaid EMA 10 (purple) and EMA 30 (orange).
  - Buy (green triangle) and Sell (red triangle) trade markers.
  - RSI sub-panel with 30/70 oversold/overbought threshold lines.
  - Summary metrics: Cumulative Return (+18.4%), Sharpe Ratio (1.82), Max Drawdown (-4.2%), Win Rate (68%).
  - Trade execution ledger detailing every round trip.

### Step 4: Machine Learning Inference (1 minute)
- Click **Explainable AI (XAI)** tab.
- Review the Dual Model Predictions:
  - XGBoost Gradient Boosted Classifier: 68% Bullish.
  - PyTorch Deep MLP: 65% Bullish.
  - Cross-model consensus confirms strong directional momentum.

### Step 5: Explainable AI Attributions (SHAP + LIME) (2 minutes)
- Point out the real SHAP TreeExplainer feature attributions:
  - Top positive contributors: RSI (14) at 58.4, EMA 10/30 ratio at 1.024.
  - Negative drag: Volatility (ATR).
- Compare with LIME local linear surrogate rules.
- Walk through the **Slide 9 Empirical Evaluation Table**:
  - Point out that SHAP wins across Fidelity (0.984 vs. 0.891), Stability (0.952 vs. 0.843), Consistency (0.912 vs. 0.825), Robustness (0.965 vs. 0.880), Sparsity (0.720 vs. 0.650), and Latency (48.2 ms vs. 112.5 ms).
  - Explain the theoretical rationale: TreeExplainer computes exact cooperative game theory Shapley values using tree structure traversal without sampling noise.

### Step 6: Groww-Inspired Paper Broker (1 minute)
- Click **Paper Broker** tab.
- Highlight virtual capital (₹10,00,000 baseline), available cash, and portfolio equity.
- Execute a manual paper trade (Buy 25 shares of TCS).
- Observe instant order update in the Order Book (`ORD-XXXXXX`) and live entry in the Double-Entry Audit Trail (`AUD-XXXX`).
- Show that cash is deducted by exact share price $\times$ quantity + fees ($₹15$).

### Step 7: Historical Simulation Replay & MongoDB Verification (1 minute)
- Run a 365-day historical simulation replay.
- Show `07_mongodb_compass_or_cli.png` or run `mongosh quantlens_xai --eval "db.paper_orders.countDocuments()"` in terminal to prove live NoSQL persistence.
