# QuantLens-XAI — Complete Visual Demo Storyboard

This document defines the 8-stage cinematic demonstration workflow for QuantLens-XAI. Each scene maps directly to user actions, visual animations, backend streaming events, and narration points.

---

## Scene 01: Natural-Language Strategy Input & Environment Readiness

- **Scene Number:** 01
- **Purpose:** Present an imposing, technical, yet clean financial AI research workspace. Establish that a local LLM is live on Apple Silicon GPU and virtual safety controls are strictly active.
- **Screen Layout:**
  - **Top:** Header with QuantLens-XAI logo, "PAPER TRADING — VIRTUAL FUNDS ONLY" badge, local AI model badge (`LOCAL AI CONNECTED — QWEN 2.5`), virtual account balance (`₹1,00,000`), and Presentation Mode toggle.
  - **Center:** Prominent card with main title: **"Describe Your Trading Idea."** Subtitle: *"Turn plain English into an explainable, testable paper-trading strategy."*
  - **Input Box:** Large styled textarea with placeholder and syntax hints.
  - **Preset Badges:** 5 interactive example pills:
    1. EMA Crossover Strategy (10/30)
    2. RSI Momentum Filter (14, 65)
    3. Bollinger Band Mean Reversion
    4. MACD Trend Confirmation
    5. Custom Multi-Indicator Strategy
  - **Action Button:** Large prominent button: **"⚡ ANALYZE & RUN STRATEGY"** with pulse hover effect.
- **Text Displayed:**
  - Header: *"QuantLens-XAI: Explainable Algorithmic Trading Platform"*
  - Badge: *"LOCAL AI CONNECTED — QWEN 2.5:0.5B (APPLE M1 PRO METAL GPU)"*
  - Button: *"⚡ ANALYZE & RUN STRATEGY"*
- **User Action:**
  User clicks Preset 1 or types:
  > *"Paper trade RELIANCE using daily candles. Buy when EMA 10 crosses above EMA 30 and RSI 14 is below 65. Sell on an opposite crossover or a 2% stop-loss or 4% take-profit. Start with ₹1,00,000 in virtual funds. Allocate a maximum of 10% of available cash per position."*
  User clicks **"⚡ ANALYZE & RUN STRATEGY"**.
- **Backend Event:**
  `POST /api/quantlens/analyze-and-run` initiates a new run ID (`run-<timestamp>`). The server opens a Server-Sent Events (SSE) stream (`GET /api/quantlens/analysis-stream/<run_id>`).
- **Visual Animation:**
  - Button state transitions into an energetic radial glow.
  - View smoothly zooms/fades into the **Strategy Intelligence Mission Control** full-screen view.
- **Expected Transition:** Smooth fade-in of Mission Control 4-panel dashboard.
- **Error State:** If prompt is empty, input highlights in amber with *"Please describe your trading strategy before analyzing."*
- **Demo Narration:**
  *"We begin by describing our quantitative trading strategy in natural English. Notice the status indicator confirming our local LLM—Qwen 2.5 running on Apple Silicon GPU—and strict virtual paper trading boundaries. Now, I will click 'Analyze & Run Strategy'."*
- **Screenshot Reference:** `docs/demo-experience/screenshots/01_strategy_input_screen.png`

---

## Scene 02: Strategy Intelligence Mission Control & Real-Time Processing

- **Scene Number:** 02
- **Purpose:** Provide an unforgettable, full-screen command center demonstrating real-time parsing, validation, and multi-stage execution telemetry.
- **Screen Layout:**
  - **Left Panel (Processing Pipeline):** 8 stages with progress icons, status dots, and connecting traces:
    01. Natural Language Understanding
    02. Strategy Extraction
    03. Rule Validation
    04. Risk Assessment
    05. Market Data Preparation
    06. ML/XAI Analysis
    07. Backtesting and Simulation
    08. Results Ready
  - **Center Panel (Active Intelligence Visualization):**
    - Dynamic stage visualizer: Neural network connection nodes pulsating while LLM computes.
    - Rule extraction visualization animating parsed tokens into structured cards.
  - **Right Panel (Live Discoveries & Warnings):** Live badges popping into view:
    - `Symbol: RELIANCE.NS`
    - `Timeframe: Daily`
    - `Dual EMA: 10 / 30`
    - `RSI Filter: < 65.0`
    - `Stop-Loss: 2.0% | Take-Profit: 4.0%`
    - `Max Allocation: 10.0%`
  - **Bottom Panel (Activity & Status Log):** Real-time terminal log emitting microsecond-timestamped application events.
- **Text Displayed:**
  - *"STRATEGY INTELLIGENCE MISSION CONTROL — RUN #run-XXXX"*
  - Status items: *"Local model returned structured strategy"*, *"Indicator parameters validated"*, etc.
- **User Action:** User observes live streaming updates or clicks any completed stage on the left to inspect its artifacts.
- **Backend Event:**
  SSE stream emits stages 1 through 8 with `RUNNING` and `COMPLETED` states, passing telemetry payloads.
- **Visual Animation:**
  - Neural nodes glow with cyan wave pulses.
  - As each stage finishes, its status pip turns emerald green with a subtle checkmark ripple.
  - Cards in the right panel slide in with a soft stagger (`translate3d(0, 0, 0)`).
- **Expected Transition:** Transitions dynamically through stages 01 to 08, unlocking the full strategy explorer.
- **Error State:** If Ollama daemon is offline, Stage 1 emits `CACHED` / `FALLBACK` with an amber badge *"Local Ollama Offline — Verified Deterministic Engine Active"*.
- **Demo Narration:**
  *"As soon as Run is clicked, Mission Control takes over. On the left, you see the 8-stage pipeline. In the center, our local LLM parses the English text into formal mathematical structures. On the right, verified parameters populate in real time, while the bottom log records every backend timestamp."*
- **Screenshot Reference:** `docs/demo-experience/screenshots/02_mission_control.png`

---

## Scene 03: Interactive Strategy Extraction & Decision Flow Graph

- **Scene Number:** 03
- **Purpose:** Demonstrate complete algorithmic transparency. Show the exact mapping from English tokens to formal rule trees and an interactive flowchart of how the engine makes trading decisions.
- **Screen Layout:**
  - **Top Half:** Side-by-side Strategy Extraction View:
    - Left: Natural English text with highlighted token pills (`RELIANCE`, `EMA 10`, `EMA 30`, `RSI < 65`, `2% STOP-LOSS`, `4% TAKE-PROFIT`).
    - Right: Interactive parsed rule cards connecting with directional relationship arrows:
      `EMA(10) --crosses above--> EMA(30) --AND--> RSI(14) < 65 ==> BUY SIGNAL`.
  - **Bottom Half:** Interactive Decision Flowchart:
    `MARKET DATA -> CALCULATE INDICATORS -> CHECK EMA CROSSOVER -> CHECK RSI CONDITION -> EVALUATE RISK RULES -> GENERATE SIGNAL -> PAPER ORDER ELIGIBILITY`.
  - **Interactive Drawer:** Clicking any node reveals live evaluation math (e.g. Current EMA10 = 1352.4, EMA30 = 1341.2, Crossover = TRUE).
- **Text Displayed:**
  - *"Interactive Strategy Extraction & Decision Logic"*
  - *"Click any rule card or flowchart node to inspect parameter definitions and evaluation logic."*
- **User Action:** User clicks on the `EMA Crossover` card and the `RSI Filter` node to inspect details.
- **Backend Event:** Uses the parsed `StrategyDefinition` and decision trace from the active run.
- **Visual Animation:** Hovering over a token highlights its corresponding rule card with an electric cyan border glow.
- **Expected Transition:** Smooth expansion of the node inspection drawer.
- **Error State:** In case of contradictory rules, node illuminates with red border and error explanation.
- **Demo Narration:**
  *"Here is our Strategy Extraction visualizer. Notice how each phrase in our English input maps directly to a verified mathematical condition. Clicking on any block in our decision flowchart displays the exact evaluation logic our backtest and paper broker execute."*
- **Screenshot Reference:** `docs/demo-experience/screenshots/03_strategy_extraction_flowchart.png`

---

## Scene 04: QuantLens Risk Intelligence & AI Strategy Advisor

- **Scene Number:** 04
- **Purpose:** Expose institutional-grade risk controls and educational AI guidance before executing any trades.
- **Screen Layout:**
  - **Left Section (QuantLens Risk Intelligence):**
    - Risk Overview Gauge: `OVERALL RISK LEVEL: MODERATE`
    - Grid of 6 Risk Factor Cards:
      1. Capital Allocation: `10.0% Max Cash` (LOW)
      2. Drawdown Exposure: `1.44% Historical Max DD` (LOW)
      3. Stop-Loss Configuration: `2.0% Fixed Stop` (CONTROLLED)
      4. Take-Profit Ratio: `4.0% (2.0x Reward:Risk)` (FAVORABLE)
      5. Market Regime Sensitivity: `Sideways Market Choppiness` (WARNING - AMBER)
      6. Execution Risk: `0.05% Slippage + 0.05% Fee Modeled` (REALISTIC)
    - Animated Warning Card:
      *"⚠️ WARNING: Sideways & Choppy Market Exposure — Dual EMA crossover systems inherently experience whipsaws in rangebound conditions. Transaction costs may erode small gains."*
    - Action Controls: `[Explain This Risk]` `[Review Risk Settings]` `[Continue With Current Rules]`
  - **Right Section (QuantLens AI Strategy Advisor):**
    - Progressive text panel organized into 7 segments:
      1. Strategy Overview
      2. Entry Logic Rationale
      3. Exit Logic Mechanics
      4. Capital Management
      5. Market Scenarios
      6. Risk Observations
      7. Suggested Improvements (e.g. Dynamic ATR Trailing Stop, Volume Confirmation)
    - Contextual Assistant input with one-click questions:
      `"Why is RSI used here?"`, `"What happens in choppy markets?"`, `"Why 10/30 EMA?"`
- **Text Displayed:**
  - *"QuantLens Risk Intelligence — Pre-Trade Structural Assessment"*
  - *"QuantLens AI Strategy Advisor — Educational Guidance & Sanity Checks"*
- **User Action:** User clicks `"Why is RSI used here?"` to inspect immediate grounded answer, then clicks `[Continue With Current Rules]`.
- **Backend Event:** AI advisory payload rendered from `quantlens.llm_parser.generate_ai_advisory`.
- **Visual Animation:** Warning card smoothly unfolds with an amber border glow. Advisor text reveals progressively.
- **Expected Transition:** Next tab illuminates, inviting historical backtest inspection.
- **Error State:** If validation fails, critical red card appears with exact rule failure details.
- **Demo Narration:**
  *"QuantLens does not execute blindly. The Risk Intelligence engine screens for regime vulnerabilities—here alerting us to sideways market whipsaws—while the AI Advisor provides educational rationale and suggests dynamic ATR improvements."*
- **Screenshot Reference:** `docs/demo-experience/screenshots/04_risk_intelligence_advisor.png`

---

## Scene 05: XGBoost & PyTorch AI Showdown

- **Scene Number:** 05
- **Purpose:** Compare traditional machine learning (XGBoost) against deep learning (PyTorch MLP) on the identical historical market bar.
- **Screen Layout:**
  - **Banner:** **"TWO MODELS. ONE MARKET. DIFFERENT PERSPECTIVES."**
  - **Top Metadata Strip:** Instrument: `RELIANCE.NS` | Sample Date: `2026-10-23` | Active Features: `8 Indicators`
  - **Left Card (XGBoost - Machine Learning):**
    - Architecture: Gradient Boosted Trees (`xgboost_reliance.json`)
    - Test Accuracy: `61.8%` | F1-Score: `0.612`
    - Prediction: `HOLD` (Confidence: `54.2%`)
    - Inference Time: `1.2 ms`
  - **Right Card (PyTorch MLP - Deep Learning):**
    - Architecture: 3-Layer Dense Neural Net with ReLU (`pytorch_mlp_reliance.pt`)
    - Device: `Apple Silicon Metal GPU / MPS`
    - Test Accuracy: `60.4%` | F1-Score: `0.598`
    - Prediction: `HOLD` (Confidence: `58.9%`)
    - Inference Time: `2.4 ms`
  - **Center Synthesis Badge:**
    - `CONSENSUS: MODELS AGREE (HOLD)`
    - Explanation: *"Both models project neutral short-term momentum; tree-based splits prioritize intermediate EMA distance while the neural net dampens extreme RSI signals."*
- **Text Displayed:**
  - *"AI Model Showdown: Machine Learning vs Deep Learning"*
- **User Action:** User toggles between sample dates or views prediction breakdown.
- **Backend Event:** Evaluates models via `ModelManager.predict_sample`.
- **Visual Animation:** Side-by-side cards slide in from opposite sides, meeting at the consensus badge with a subtle lock-in sound/pulse.
- **Expected Transition:** Flow moves into the explainability explorer.
- **Demo Narration:**
  *"Here we pit two distinct AI paradigms against each other. On the left, XGBoost; on the right, PyTorch MLP running on Metal GPU. Notice that rather than manufacturing artificial agreement, QuantLens measures real cross-model consensus."*
- **Screenshot Reference:** `docs/demo-experience/screenshots/05_ml_showdown.png`

---

## Scene 06: Interactive SHAP & LIME Explainability Explorer

- **Scene Number:** 06
- **Purpose:** Deliver the core XAI research capability. Reveal real SHAP TreeExplainer attributions, LIME local surrogate weights, Slide 9 empirical evaluation metrics, and interactive cross-linking.
- **Screen Layout:**
  - **Heading:** **"Why Did the AI Make This Prediction?"**
  - **Subheading:** *"Mathematical feature attribution for the selected model prediction."*
  - **Dual Attribution Visualizer:**
    - **Left: SHAP (Shapley Additive exPlanations):** Horizontal waterfall bar chart showing exact Shapley contributions toward class prediction. Positive (green) vs negative (orange-red) forces.
    - **Right: LIME (Local Interpretable Model-agnostic Explanations):** Local linear surrogate weights with rule boundary thresholds (`-0.27 < rsi_14 <= 0.49`).
  - **Slide 9 Empirical Metrics Suite:**
    - Spearman Rank Correlation: `ρ = 0.302`
    - Top-3 Feature Agreement: `0.0%`
    - Local Fidelity: `R² = 0.086`
    - Stability Score: `0.941`
    - Robustness (Perturbation Stability): `0.912`
    - Explanation Latency: `SHAP: 1.23 ms | LIME: 142.1 ms`
  - **Interactive Cross-Linking Feature:**
    Clicking any feature (e.g. `rsi_14`) instantly highlights it across:
    1. SHAP bar chart
    2. LIME bar chart
    3. Technical indicator candlestick chart
    4. Explanatory interpretation card
- **Text Displayed:**
  - *"Cross-Explainer Consistency: Spearman ρ = 0.302"*
  - *"Feature Highlight: rsi_14 (Relative Strength Index lookback 14) acts as a cooling mechanism preventing overbought entries."*
- **User Action:** User clicks on the `rsi_14` feature bar; observes simultaneous highlight on all panels.
- **Backend Event:** Fetches real attributions via `/api/quantlens/xai-explain`.
- **Visual Animation:** Bars expand horizontally from zero baseline using ease-out cubic animation.
- **Expected Transition:** User transitions to the guided historical backtest.
- **Demo Narration:**
  *"This is the explainability core of QuantLens. On the left, exact cooperative game-theoretic SHAP attributions; on the right, LIME surrogate rules. Notice that when I click 'rsi_14', the system cross-links the feature across the SHAP plot, LIME plot, and candlestick chart. We also report all six Slide 9 empirical evaluation metrics."*
- **Screenshot Reference:** `docs/demo-experience/screenshots/06_xai_explainability.png`

---

## Scene 07: Guided Historical Backtest & Strategy Event Replay

- **Scene Number:** 07
- **Purpose:** Showcase deterministic financial performance with interactive playback controls, candlestick markers, and animated KPI counters.
- **Screen Layout:**
  - **Stage 1 (Dataset Banner):** `RELIANCE.NS` | `1,687 Daily Candles` | `Zero Look-Ahead Bias Verified`
  - **Stage 2 (Chart Header & Playback Controls):**
    - Buttons: `[▶ Play]` `[⏸ Pause]` `[↺ Restart]` `[1x]` `[2x]` `[4x]` `[⏭ Next Signal]`
  - **Stage 3 (Interactive Candlestick & Indicator Chart):**
    - ApexCharts candlestick series with EMA(10) (cyan line), EMA(30) (violet line), and RSI(14) lower oscillator.
    - Green upward triangles for BUY entries; Red downward triangles for SELL exits.
    - Floating Signal Tooltip showing candle timestamp, indicator crossover values, and trigger reason.
  - **Stage 4 (Financial KPI Cards with Animated Counters):**
    - Cumulative Return: `+0.20%`
    - Win Rate: `37.04%` (10 Wins / 17 Losses)
    - Max Drawdown: `-1.44%`
    - Sharpe Ratio: `-1.17` | Sortino Ratio: `-0.55`
    - Total Trades: `27 Trades` | Profit Factor: `1.03`
  - **Approve Strategy Banner:**
    Prominent button: **"🚀 DEPLOY TO QUANTLENS PAPER BROKER"**
- **Text Displayed:**
  - *"Historical Backtest: 1,687 Daily Candles Analyzed"*
  - *"Deterministic Event-Driven Simulation — Zero Fabricated Trades"*
- **User Action:** User clicks `[▶ Play]` to watch playback, or clicks `[⏭ Next Signal]` to jump to an entry, then clicks **"🚀 DEPLOY TO QUANTLENS PAPER BROKER"**.
- **Backend Event:** Executed via `run_strategy_backtest` (`/api/quantlens/backtest`).
- **Visual Animation:** Candlestick chart advances smoothly across bars; numeric counters tick up from zero to actual calculated metrics.
- **Expected Transition:** Cinematic collapsing animation into the Paper Broker view.
- **Demo Narration:**
  *"Here we run our deterministic historical backtest. We can replay events at 1x, 2x, or 4x speed. Notice the animated KPI counters ending at true mathematical outputs: 27 trades executed with a 1.44% maximum drawdown. Now, let's deploy the approved strategy to the Paper Broker."*
- **Screenshot Reference:** `docs/demo-experience/screenshots/07_historical_backtest.png`

---

## Scene 08: Cinematic Transition, Groww-Inspired Paper Broker & Persistence Proof

- **Scene Number:** 08
- **Purpose:** Bridge the research phase into live paper execution with simulated orders, portfolio updates, and hybrid SQL/NoSQL database persistence proof.
- **Screen Layout:**
  - **Cinematic Transition Overlay:** Strategy card collapses and docks into the Paper Broker console:
    `STRATEGY VALIDATED -> SIMULATION ENGINE READY -> PAPER BROKER CONNECTED -> VIRTUAL ACCOUNT LOADED -> READY FOR REPLAY`.
  - **Paper Broker Console:**
    - Top Metrics: Initial Virtual Capital `₹1,00,000` | Cash `₹99,603.53` | Invested `₹0.00` | Realized P&L `-₹396.47`
    - Replay Action: `[▶ Run 60-Bar Historical Replay]` button.
    - Live Order Execution Overlay:
      When a BUY/SELL triggers during replay:
      - Pulse highlight on candle
      - Floating receipt: `PAPER BUY EXECUTED: RELIANCE.NS | 7 Shares @ ₹1,294.25 | Fee: ₹4.53 | Slippage: 0.05%`
    - Tabbed Ledgers:
      - Open Positions Table (0 positions)
      - Orders Ledger Table (4 executed orders with unique IDs e.g. `ORD-523267`)
      - Immutable Strategy-to-Order Audit Trail Table (with timestamps and rule reasons)
  - **System Inspector Drawer (Database Persistence Proof):**
    - SQLite Section: 6 active tables, zero corruption, relational audit entries.
    - MongoDB Section: Database `quantlens_xai`, collections `paper_accounts` (1), `paper_orders` (4), `paper_audit_events` (5), `xai_evaluation_results` (1).
    - Persistence Demo Button: `[Verify MongoDB State]` verifies that state survives page reload.
  - **Final Action Button:** **"📊 VIEW FINAL STRATEGY ANALYSIS REPORT"**
- **Text Displayed:**
  - *"QuantLens Paper Broker — Virtual Trading Execution Venue"*
  - *"Hybrid Architecture Verified: SQLite 3 Relational + MongoDB Community 7.0 NoSQL"*
- **User Action:** User clicks `[▶ Run 60-Bar Historical Replay]`, observes live execution popups, inspects MongoDB records, and clicks **"📊 VIEW FINAL STRATEGY ANALYSIS REPORT"**.
- **Backend Event:** `POST /api/quantlens/paper-broker/replay` executes simulated trading and persists records to MongoDB.
- **Visual Animation:** Cash counters animate downward on purchases and update on sales. Order receipt flashes emerald green for fill.
- **Expected Transition:** Final comprehensive strategy report screen opens.
- **Demo Narration:**
  *"The strategy is now live in our Paper Broker. We run a 60-bar historical replay. Notice how simulated orders generate fill receipts with realistic brokerage fees and slippage. In the System Inspector, you can verify real-time persistence across both SQLite and MongoDB Community 7.0."*
- **Screenshot Reference:** `docs/demo-experience/screenshots/08_paper_broker_persistence.png`

---

## Scene 09: Final Interactive Strategy Analysis Report

- **Scene Number:** 09
- **Purpose:** Provide an executive-level summary tying all stages of the demonstration together into a presentation-ready wrap-up.
- **Screen Layout:**
  - **Hero Title:** **"YOUR STRATEGY, FULLY ANALYZED."**
  - **6 Structured Synthesis Cards:**
    1. **Strategy Specification Card:** Symbol, dual EMA periods, RSI thresholds, risk boundaries, model used.
    2. **AI Interpretation Card:** Assumptions made, regime caveats, recommended ATR improvements.
    3. **Model Showdown Summary:** XGBoost vs PyTorch prediction consensus.
    4. **Explainable AI Card:** Top contributing features from SHAP & LIME, Slide 9 Spearman correlation.
    5. **Financial Performance Card:** Backtest metrics, equity curve snapshot, max drawdown.
    6. **Paper Execution Card:** Starting virtual funds, ending equity, completed trades, audit verification.
  - **Action Controls:**
    - `[📥 Export Analysis Report (JSON/Markdown)]`
    - `[↺ Reset Demo for New Presentation]`
    - `[🎯 Return to Strategy Builder]`
- **Text Displayed:**
  - *"Executive Quantitative & XAI Summary"*
  - *"Full academic audit trail preserved in MongoDB database 'quantlens_xai'."*
- **User Action:** User clicks `[📥 Export Analysis Report]` or `[↺ Reset Demo for New Presentation]`.
- **Backend Event:** Synthesizes complete run payload; demo reset resets MongoDB to fresh ₹1,00,000.
- **Visual Animation:** Cards cascade into view with staggered fade-and-lift motion (`opacity: 0 -> 1`, `transform: translateY(20px) -> 0`).
- **Demo Narration:**
  *"To conclude, here is our complete strategy summary card. Every layer—from natural language parsing to mathematical validation, dual ML modeling, XAI attributions, backtesting, and paper execution—is documented with full technical integrity."*
- **Screenshot Reference:** `docs/demo-experience/screenshots/09_final_strategy_report.png`
