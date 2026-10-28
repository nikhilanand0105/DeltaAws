# QuantLens-XAI — Official Faculty Demonstration Script

**Project Title:** QuantLens-XAI: Explainable Algorithmic Trading Platform with Local LLM Reasoning and Multi-Model XAI  
**Target Duration:** 4 to 6 minutes  
**Presenter:** Nikhil Anand (BCSE418L Academic Year 2026–27)  
**Execution Environment:** Apple MacBook Pro M1 Pro (16 GB Unified Memory), Local Ollama LLM, Hybrid SQLite + MongoDB Community 7.0  

---

## 00:00 – 00:45 | Scene 1: Introduction & Natural-Language Strategy Input

### What I Do:
1. Open the browser at `http://127.0.0.1:5001/quantlens`.
2. Point cursor to the top status badges: `LOCAL AI CONNECTED — QWEN 2.5` and `PAPER TRADING — VIRTUAL FUNDS ONLY`.
3. Click on the first preset card: **"EMA Crossover Strategy (10/30) with RSI Momentum Filter"**.
4. The natural language prompt populates the input textarea:
   > *"Buy RELIANCE when EMA 10 crosses above EMA 30 and RSI is below 65, exit on reverse crossover or 2% stop loss, 4% take profit with 10% max capital allocation."*
5. Hover over the large glowing button: **"⚡ ANALYZE & RUN STRATEGY"**.

### What I Say:
> *"Good morning, Professor. Welcome to QuantLens-XAI. Our objective is to take unstructured natural language trading ideas and transform them into mathematically validated, explainable, and testable algorithmic trading strategies—without ever leaving our local machine or risking real capital.*  
> *Notice our environment header: we are running a local Qwen 2.5 LLM accelerated via Apple Silicon Metal GPU, connected to an immutable MongoDB 7.0 database, and strictly isolated in virtual paper trading mode.*  
> *I have selected a classic institutional trend-following strategy on RELIANCE equity. Now, let’s watch the quantitative intelligence engine analyze our strategy."*

### What I Do:
- Click **"⚡ ANALYZE & RUN STRATEGY"**.

---

## 00:45 – 01:30 | Scene 2: Strategy Intelligence Mission Control & Strategy Extraction

### What Appears:
- The screen dynamically transitions into the full-screen **Strategy Intelligence Mission Control**.
- The left pipeline lights up through stages: Natural Language Understanding, Strategy Extraction, Rule Validation, Risk Assessment.
- The center visualizer dissects the English text into tokens and draws the mathematical rule tree.
- The right panel lists verified discoveries (`Symbol: RELIANCE.NS`, `EMA: 10/30`, `SL: 2%`, `TP: 4%`).
- The bottom terminal log streams real-time microsecond-level timestamps.

### What I Say:
> *"Immediately upon clicking Run, Mission Control takes over. This is not a simulated video—it is an event-driven Server-Sent Events stream from our Flask backend. On the left, our 8-stage pipeline tracks execution. In the center, our local LLM parsed the English text into formal Pydantic rules.*  
> *Notice the visual relationship diagram: EMA 10 must breach EMA 30 upward, conditioned by RSI below 65. If I click on any rule card, we can inspect its exact mathematical parameter definition, the source phrase from our prompt, and why the engine enforces it."*

---

## 01:30 – 02:15 | Scene 3: Risk Intelligence & Contextual AI Strategy Advisor

### What I Do:
- Click the **"Risk & Advisor"** tab or section in Mission Control.
- Point to the **QuantLens Risk Intelligence** overview cards.
- Point to the amber warning card: `WARNING: Sideways Market Exposure`.
- Click the quick question in the Advisor: `"Why is RSI used here?"`.

### What Appears:
- The Risk Intelligence panel shows: Capital Allocation (10% - LOW), Drawdown (1.44% - LOW), Risk-to-Reward Ratio (2.0x - FAVORABLE), and Market Regime Risk (AMBER).
- The AI Advisor instantly displays the grounded rationale:
  *"EMA(10) reacts quickly to short-term momentum while EMA(30) smooths out noise. Requiring RSI < 65 prevents entering at the overbought exhaustion peak of a price impulse."*

### What I Say:
> *"Before risking virtual capital, QuantLens conducts a structural risk audit. Notice the amber alert: the engine warns us that dual EMA crossover systems suffer high whipsaw rates in sideways, rangebound markets. It flags this regime risk explicitly.*  
> *Simultaneously, the AI Advisor provides educational guidance. When I ask 'Why is RSI used here?', it explains that the RSI ceiling acts as an exhaustion filter to prevent buying into an overextended rally."*

---

## 02:15 – 03:00 | Scene 4: Machine Learning Showdown (XGBoost vs PyTorch MLP)

### What I Do:
- Navigate to the **"AI Model Showdown"** view.
- Compare the two side-by-side cards: XGBoost on the left, PyTorch MLP on the right.

### What Appears:
- **XGBoost:** Tree-based classifier, 61.8% test accuracy, prediction: `HOLD` (54.2% confidence).
- **PyTorch MLP:** 3-layer deep neural network on Metal GPU, 60.4% test accuracy, prediction: `HOLD` (58.9% confidence).
- Central Consensus Badge: `CONSENSUS: MODELS AGREE (HOLD)`.

### What I Say:
> *"Now we compare two distinct artificial intelligence paradigms on the exact same historical candle. On the left is XGBoost—gradient boosted decision trees; on the right is a PyTorch Multi-Layer Perceptron trained on Apple Silicon MPS.*  
> *Both models output a HOLD consensus on this recent candle. Rather than manufacturing artificial agreement, QuantLens measures real cross-model alignment, allowing researchers to detect when deep learning and decision trees diverge."*

---

## 03:00 – 03:50 | Scene 5: Interactive SHAP & LIME Explainability Explorer

### What I Do:
- Scroll to the **"Why Did the AI Make This Prediction?"** section.
- Point to the left SHAP waterfall chart and right LIME surrogate weights chart.
- Click on the feature bar for `rsi_14`.

### What Appears:
- SHAP bar chart highlights `rsi_14` with its exact Shapley value.
- LIME chart simultaneously highlights `rsi_14` with its surrogate rule (`-0.27 < rsi_14 <= 0.49`).
- The price candlestick chart simultaneously highlights the RSI indicator panel.
- The Slide 9 Empirical Metrics table displays: Spearman Rank Correlation `ρ = 0.302`, Fidelity `R² = 0.086`, Stability `0.941`, and Robustness `0.912`.

### What I Say:
> *"Here is the core XAI contribution of the project. On the left, we compute exact Shapley attributions using SHAP TreeExplainer; on the right, local surrogate explanations via LIME TabularExplainer.*  
> *Notice what happens when I click on 'rsi_14': the platform cross-links this feature simultaneously across the SHAP waterfall, the LIME weights, and our technical indicator chart. We also report all six Slide 9 empirical evaluation metrics—validating fidelity, stability, robustness, and a cross-explainer rank correlation of 0.302."*

---

## 03:50 – 04:35 | Scene 6: Guided Historical Backtest with Playback Controls

### What I Do:
- Switch to the **Historical Backtest** view.
- Click `[▶ Play]` and toggle to `[2x]` speed.
- Click `[⏭ Next Signal]` to jump directly to a Golden Cross entry marker.
- Point to the animated numeric counters for Sharpe Ratio, Max Drawdown, and Win Rate.
- Click the large button: **"🚀 DEPLOY TO QUANTLENS PAPER BROKER"**.

### What Appears:
- The chart animates across 1,687 daily candles of RELIANCE historical data.
- Green upward triangles indicate Golden Cross entries; red downward triangles indicate Stop-Loss or Death Cross exits.
- Animated counters reach: Cumulative Return `+0.20%`, Win Rate `37.04%`, Max Drawdown `-1.44%`, Total Trades `27`.
- Clicking Deploy triggers the cinematic transition into the Paper Broker console.

### What I Say:
> *"Here is our deterministic, event-driven backtesting engine operating over 1,687 daily candles of historical RELIANCE data. We have full playback controls—play, pause, 1x, 2x, 4x, or skip to the next signal.*  
> *All calculated metrics—Sharpe ratio, 1.44% max drawdown, and 27 executed trades—are strictly mathematical with zero look-ahead bias. With our strategy validated, let’s deploy it into our Paper Broker."*

---

## 04:35 – 05:20 | Scene 7: Paper Broker Replay, Simulated Orders & Persistence Proof

### What I Do:
- Arrive at the Groww-inspired **QuantLens Paper Broker**.
- Point to the initial virtual balance: `₹1,00,000.00`.
- Click **"▶ Run 60-Bar Historical Replay"**.
- Watch the simulated trade execution overlay appear: `PAPER BUY EXECUTED: RELIANCE | 7 Shares @ ₹1,294.25`.
- Open the **System Inspector (Technical View)** drawer.

### What Appears:
- Historical replay executes 59 bars.
- 4 real simulated orders execute, factoring in 0.05% brokerage fees and 0.05% slippage.
- Cash updates to `₹99,603.53`. Orders Ledger records order `ORD-523267`.
- Audit Trail logs 5 immutable events.
- System Inspector displays:
  - SQLite: 6 tables active in `instance/local.db`.
  - MongoDB Community 7.0: `paper_accounts` (1), `paper_orders` (4), `paper_audit_events` (5), `xai_evaluation_results` (1).

### What I Say:
> *"Now we are inside our simulated brokerage venue. I click 'Run Historical Replay'. In real time, the engine evaluates our validated EMA-RSI rules against daily candles, generating genuine virtual buy and sell orders.*  
> *Notice our execution overlay: 7 shares of RELIANCE were purchased, calculating exchange turnover fees and execution slippage. Cash is conserved with double-entry accounting.*  
> *To prove technical integrity, look at our System Inspector: every single order, position, and audit event is durably persisted in MongoDB Community 7.0 alongside our SQLite relational tables."*

---

## 05:20 – 05:45 | Scene 8: Final Strategy Analysis Report & Conclusion

### What I Do:
- Click **"📊 VIEW FINAL STRATEGY ANALYSIS REPORT"**.
- Point to the executive synthesis cards (Strategy, AI Interpretation, Model Showdown, Financial Analysis, Paper Broker, Persistence).
- Click `[↺ Reset Demo]` to show instant reproducibility.

### What I Say:
> *"To conclude, QuantLens-XAI synthesizes the entire research lifecycle into an executive strategy report. Every step—from natural language parsing to mathematical rule verification, dual ML modeling, game-theoretic explainability, backtesting, and virtual broker execution—is transparent, auditable, and grounded in real computation.*  
> *Thank you, Professor. I am now open to your questions."*

---

## Faculty Q&A Reference Guide

### Q1: "Why did you use both SQLite and MongoDB?"
> **Answer:** *"QuantLens uses a hybrid architecture for separation of concerns. SQLite manages structured relational tables such as user settings, core account configurations, and system flags where ACID schema guarantees are paramount. MongoDB Community 7.0 handles high-throughput, flexible document data—including variable indicator parameter schemas, granular trade ledgers, cryptographic audit logs, and cached high-dimensional SHAP/LIME explanation matrices."*

### Q2: "Does SHAP explain the trading rule or the machine learning model?"
> **Answer:** *"SHAP and LIME explain the predictions of our machine learning models (XGBoost and PyTorch MLP). They quantify how features like RSI and EMA distance influence the model's forward-looking classification (BUY, SELL, or HOLD). The trading strategy itself uses deterministic rule-based logic (such as moving average crossovers). In QuantLens, we explicitly distinguish between rule validation and ML feature attribution to prevent deceptive oversimplification."*

### Q3: "What happens if the local Ollama LLM is turned off?"
> **Answer:** *"QuantLens has a strict zero-fabrication fallback hierarchy. If Ollama is offline or uninstalled, the system clearly notifies the user, flags the runtime as offline, and falls back to a deterministic, pre-verified strategy definition template. It never invents fake LLM reasoning."*

### Q4: "How do you guarantee that no real money is ever traded?"
> **Answer:** *"The platform enforces a strict safety boundary at both the schema level (`trading_mode: 'paper'`) and the broker architecture level. The execution engine only interfaces with our internal `PaperBroker` class, which operates purely in virtual memory and MongoDB. Real-money exchange endpoints are entirely disabled."*
