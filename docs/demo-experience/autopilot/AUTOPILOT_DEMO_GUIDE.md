# QuantLens Autopilot — Live Demonstration Guide

**AI-Powered Continuous Paper Trading Simulator**  
*Heading: YOUR STRATEGY IS NOW IN CONTROL*  
*Mandatory Academic Safety Notice: PAPER TRADING — HISTORICAL REPLAY / VIRTUAL MONEY*

---

## 1. Feature Overview & Purpose

**QuantLens Autopilot** transforms static natural-language trading rules into an autonomous, causal financial simulation command center. Rather than presenting static tabular backtest summaries or disjointed batch execution, Autopilot provides an interactive, candle-by-candle playback experience where viewers observe an algorithmic system actively evaluating market dynamics, monitoring risk guards, making reasoned decisions (BUY, SELL, or HOLD), and executing virtual orders with strict double-entry accounting.

Autopilot operates strictly with virtual funds (starting capital: ₹1,00,000.00). It is connected directly to the authoritatively managed `PaperBroker` and durably logs every execution, condition evaluation, and portfolio state transition to MongoDB Community 7.0 (`quantlens_xai` database).

---

## 2. Architectural Design Philosophy

1. **Authoritative Backend Execution:** All mathematical indicator computations, crossover detection, stop-loss / take-profit monitoring, position sizing, and marked-to-market portfolio accounting occur strictly on the Python backend (`quantlens/autopilot_engine.py` and `quantlens/paper_broker.py`). The browser client acts as an interactive cockpit, preventing client-side drift or lookahead bias.
2. **Causal Progression (Zero Lookahead Bias):** Candles are evaluated one by one strictly in historical chronological order. At candle $t$, the system has access only to bars $0 \dots t$.
3. **HOLD as an Active Algorithmic Decision:** A non-trading candle is not silence—it is an explicit decision to maintain capital in virtual cash or monitor an open position. Autopilot renders real-time rationale for HOLD decisions on every single candle.
4. **Transparent Explainability (XAI):** Every filled order is backed by an interactive "WHY DID THIS TRADE HAPPEN?" drawer detailing the mathematical rule trace, machine learning model confidence (XGBoost & PyTorch MLP), SHAP feature attributions, LIME surrogate conditions, and grounded English narrative.
5. **Double-Entry Cash Conservation:** Every virtual transaction rigorously accounts for brokerage fees (0.05%) and execution slippage (0.05%), ensuring:
   $$\text{Portfolio Value} = \text{Virtual Cash} + \sum (\text{Shares} \times \text{Current Price})$$
   $$\text{Cash Balance} = \text{Starting Capital} - \sum \text{Cash Invested} + \sum \text{Proceeds} - \sum \text{Fees}$$

---

## 3. Screen Layout & Command Center Zones

```
+----------------------------------------------------------------------------------------------------+
| QUANTLENS AUTOPILOT [STATUS: RUNNING] • REPLAY DATE: 2026-05-18 • [AUDIO: ON] • [PRESENTATION MODE] |
| Controls: [▶ Play] [⏯ Step] [⏭ Skip to Signal] [↺ Restart] | Speed: [1x] [2x] [4x] [8x] | Scenario: [A]   |
+----------------------------------------------------------------------------------------------------+
| KPI CARDS: Capital: ₹1,00,000 | Equity: ₹99,829.22 | Cash: ₹99,829.22 | Un. P&L: ₹0 | Ret: -0.17%    |
+----------------------------------------------------------------------------------------------------+
| WHAT QUANTLENS IS DOING RIGHT NOW: "Monitoring RELIANCE daily candles. Fast EMA > Slow EMA..."       |
+-------------------------------------------------------------------+--------------------------------+
| LEFT (60%): Interactive Candlestick & Indicator Chart              | RIGHT (40%):                   |
| - OHLCV Daily Candlesticks                                        | 1. Active Position Card        |
| - Fast EMA 10 (Cyan) & Slow EMA 30 (Purple)                       |    (Shares, Avg, Current, SL)  |
| - RSI 14 (Amber Subplot)                                          | 2. Recent Paper Executions     |
| - Execution Markers (BUY / SELL) & Dynamic SL/TP Lines            |    (Orders + "🔍 Explain")     |
|                                                                   | 3. Mini Equity Curve           |
| LIVE AI STRATEGY DECISION ENGINE (Condition-by-Condition Grid):   |    (Area chart vs ₹1,00,000)   |
| [EMA Cross: YES] [RSI: 50.0 PASSED] [Position: FLAT] [SL/TP Guard] |                                |
| [ACTION HERO: BUY ORDER • Reason: Bullish Golden Cross Detected]  |                                |
+-------------------------------------------------------------------+--------------------------------+
| BOTTOM (100%): AUTOPILOT OPERATIONAL TELEMETRY & ACTIVITY FEED                                      |
| Filter: [ALL] [DECISIONS] [ORDERS] [RISK] [EXPLANATIONS] • Auto-Scroll: [ON]                        |
| • 00:32:21 [ORDER] Paper SELL Filled: ORD-741780 (Stop-Loss Hit -1.8% <= -2.0%)                    |
| • 00:32:17 [DECISION] Bullish Golden Cross Confirmed (EMA10 1456.5 > EMA30 1456.4)                |
+----------------------------------------------------------------------------------------------------+
```

---

## 4. Pre-Configured Demonstration Scenarios

| Scenario | Asset | Window | Core Phenomenon Demonstrated |
| :--- | :--- | :--- | :--- |
| **Scenario A: Trend Following** *(Recommended Default)* | RELIANCE.NS | 120 Bars | Bullish Golden Cross breakout, RSI filter passing under 65.0, clean buy entry, profit accumulation, dynamic trailing. |
| **Scenario B: Risk Management** | RELIANCE.NS | 80 Bars | High market volatility and sharp correction. Demonstrates automated stop-loss liquidation to protect capital. |
| **Scenario C: Extended Autopilot** | RELIANCE.NS | 240+ Bars | Long-horizon multi-cycle trading through alternating trends, whipsaws, and ranging regimes. |
| **Synthetic Sandbox: Trending Up** | SYNTH_ALPHA | 60 Bars | Clean geometric drift upward. Verifies mathematical execution with zero market noise. |
| **Synthetic Sandbox: Volatile** | SYNTH_BETA | 60 Bars | High stochastic variance testing allocation guards and slippage dampening. |

---

## 5. Step-by-Step Operator Instructions

### Flow 1: One-Click Launch from Strategy Composer
1. Navigate to `http://127.0.0.1:5001/quantlens`.
2. In **01. Strategy Composer**, click the prominent green button: `🤖 LAUNCH QUANTLENS AUTOPILOT`.
3. The interface seamlessly shifts to Tab 07 (`tab-autopilot`), loads Scenario A on RELIANCE with virtual ₹1,00,000, and starts autonomous candle progression.

### Flow 2: Live Playback Controls
- **Play / Pause (`btnApPlay`):** Starts and pauses the continuous playback loop.
- **Step 1 Candle (`btnApStep`):** Advances exactly one daily bar, updating indicators and decision engine cards.
- **Skip to Next Signal (`btnApSkip`):** Causally fast-forwards through intervening HOLD candles until a BUY or SELL order is executed.
- **Playback Speed:** Click `1x`, `2x`, `4x`, or `8x` to accelerate simulation velocity.
- **Sound Toggle (`btnApSoundToggle`):** Enables client-side Web Audio API synthesizer chimes (ascending for BUY, resolving for SELL, low warning for SL).

### Flow 3: Inspecting Trade Explainability
1. In the **Recent Paper Executions** panel on the right, click `🔍 Explain` on any executed order.
2. The **Trade Explainability & Verification Modal** opens, displaying:
   - Order execution metadata (fill price, shares, fee, slippage).
   - Exact mathematical condition that fired the rule.
   - Machine learning consensus (XGBoost prediction & PyTorch MLP confidence).
   - SHAP feature attributions and LIME surrogate rules.
   - AI plain-English commentary grounding the decision.
   - MongoDB storage provenance in `quantlens_xai.paper_orders`.

### Flow 4: Session Wrap-Up & Export
1. Click `📊 Session Report` in the top controls bar.
2. Review the comprehensive performance table: total bars evaluated, ending portfolio equity, net P&L, win rate %, max drawdown %, friction paid, and cash conservation proof.
3. Click `📥 Export JSON` or `📝 Export Markdown` to download persistent verification reports.
