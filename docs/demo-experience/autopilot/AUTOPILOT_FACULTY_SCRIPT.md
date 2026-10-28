# QuantLens Autopilot — Faculty Evaluation & Demonstration Script

**The Complete Oral Presentation Guide for Academic & Quantitative Defense**  
*Course: BCSE418L — Advanced Quantitative Systems & Financial Engineering*

---

## 1. Demo Setup & Readiness Checklist (T-minus 2 Minutes)

Before calling the professor or panel to the screen:
1. Ensure the Flask server is running on port 5001 (`http://127.0.0.1:5001/quantlens`).
2. Verify MongoDB Community 7.0 is active on port 27017 (`brew services list | grep mongodb`).
3. Verify Ollama is running (`curl -s http://127.0.0.1:11434/api/tags | grep qwen2.5`).
4. Open Google Chrome at `http://127.0.0.1:5001/quantlens`.
5. Maximize the browser window (or press the `🖥️ Presentation` button in the header).

---

## 2. Word-for-Word Faculty Presentation Script

### Stage 1: The Vision & Academic Context (0:00 – 1:00)

**What to Click:** Start on **01. Strategy Composer** (`http://127.0.0.1:5001/quantlens`).  
**What to Point At:** The natural-language strategy text box and the prominent banner: `PAPER TRADING — VIRTUAL FUNDS ONLY`.

**What to Say:**
> *"Good morning, Professor. Today, I am proud to present **QuantLens Autopilot**—the continuous AI paper-trading simulator inside QuantLens-XAI.*
>
> *Most financial backtesting systems in literature present static, post-hoc tables of metrics like Sharpe Ratio and cumulative returns. While mathematically useful, they completely obscure the reality of algorithmic decision-making: how a model navigates risk, monitors indicators candle-by-candle, respects capital boundaries, and decides when NOT to trade.*
>
> *We built QuantLens Autopilot to solve this problem. It takes an English trading instruction, compiles it into a validated Pydantic specification, and hands full control over to an autonomous financial simulation engine operating strictly on virtual funds with double-entry accounting."*

---

### Stage 2: Handing Over Control to Autopilot (1:00 – 2:00)

**What to Click:** Click the large green button in the composer:  
`🤖 LAUNCH QUANTLENS AUTOPILOT`.

**What to Point At:**
1. The animated pulse beside `QUANTLENS AUTOPILOT` in the header.
2. The subtitle: `AI-Powered Continuous Paper Trading Simulator` and `YOUR STRATEGY IS NOW IN CONTROL`.
3. The starting virtual capital card: `₹1,00,000.00`.
4. The scenario selector set to `Scenario A: Trend Following (RELIANCE)`.

**What to Say:**
> *"Notice what just happened. With a single click, our approved strategy was transferred into the paper trading cockpit. The system initialized a 120-day historical replay window for RELIANCE.NS, loaded ₹1,00,000 in virtual capital, and set up our double-entry ledger.*
>
> *I want to highlight that this simulation is authoritatively executed on our Python backend. The browser is not fabricating data; every bar is processed causally with strict chronological progression."*

---

### Stage 3: Continuous Autonomous Execution & Active HOLD Monitoring (2:00 – 3:30)

**What to Click:**
1. In the top controls bar, click `▶ Play Replay` (or select `2x` speed).
2. Watch the chart candlesticks advance and the performance cards update.
3. Pause after 4–5 bars by clicking `⏸ Pause Replay`.

**What to Point At:**
1. The **"WHAT QUANTLENS IS DOING RIGHT NOW"** narration banner.
2. The **LIVE AI STRATEGY DECISION ENGINE** panel below the chart:
   - Fast / Slow EMA cross indicator (`MONITORING` or `BULLISH ALIGNED`).
   - RSI Momentum Ceiling (`VALID (PASSED)` below 65.0).
   - Active Position State (`FLAT` or `LONG ACTIVE`).
   - The large badge displaying `HOLD / WAITING`.
3. The **Operational Telemetry & Activity Feed** at the bottom streaming `DATA`, `INDICATOR`, and `DECISION` events.

**What to Say:**
> *"Look at the Decision Engine card while the replay advances. On every single daily candle, the engine evaluates our two entry rules: Is the 10-day EMA above the 30-day EMA? And is RSI under 65?*
>
> *Crucially, on days where no crossover occurs, the system does not go silent. It actively issues an explicit **HOLD** decision, explaining to the user in plain English: 'Monitoring trend and boundaries. Waiting for golden cross.' In quantitative finance, deciding not to trade is an active risk management action that protects capital."*

---

### Stage 4: Order Execution, Position Management & Dynamic SL/TP (3:30 – 5:00)

**What to Click:**
1. Click `⏭ Skip to Next Signal` (or let it run until the first BUY order executes).
2. The screen displays the green toast notification: `PAPER BUY FILLED: RELIANCE.NS • 6 Shares @ ₹1,457.59`.
3. Point out the updated **Live Position Card** and the **Dynamic Stop-Loss (-2%) and Take-Profit (+4%)** lines.

**What to Point At:**
1. The **Portfolio Equity** and **Available Cash** cards updating: Virtual cash decreased by ₹8,745.54, but Total Equity remains conserved.
2. The exact execution marker on the ApexCharts candlestick series.
3. In the right-hand panel, click `🔍 Explain` on the executed order in **Recent Paper Executions**.

**What to Say:**
> *"Here is our first automated execution. The 10-day EMA crossed above the 30-day EMA at ₹1,456.46 with RSI at 50.0. The system verified our 10% maximum capital allocation rule and automatically sized the order to 6 shares.*
>
> *Notice our accounting precision: ₹4.37 was deducted for realistic 0.05% brokerage and 0.05% slippage. The remaining capital stayed in cash.*
>
> *Now let's open the trade explainability drawer by clicking 'Explain Trade'. Look at what our system reveals: Here is the exact causal mathematical rule trace, followed by our machine learning model consensus—both XGBoost and our PyTorch Deep MLP confirmed the direction. Below that, SHAP feature attributions show that EMA-30 was the primary positive driver (+0.080 weight). And finally, the record references our immutable MongoDB collection `paper_orders`."*

---

### Stage 5: Exit Discipline, Stop-Loss Defense & Session Wrap-Up (5:00 – 6:30)

**What to Click:**
1. Close the explanation modal.
2. Click `⏭ Skip to Next Signal` to observe the automated exit (Stop-loss hit at -1.8% or take-profit harvest).
3. Click `📊 Session Report` in the top controls bar.

**What to Point At:**
1. The **Session Summary Modal** displaying the complete KPI table:
   - Win Rate %, Net Return %, Max Drawdown %, Total Friction Deducted.
   - The line stating: `Cash Conserved: 100% Double-Entry Validated`.
2. The export buttons: `📥 Export JSON` and `📝 Export Markdown`.

**What to Say:**
> *"When market conditions reversed, our stop-loss rule triggered immediately, liquidating the position to cap drawdown at 1.8%. The virtual proceeds returned cleanly to available cash.*
>
> *In this Session Summary modal, you can review the complete accounting ledger. Everything has been validated against our 20-step automated test suite and persisted in MongoDB Community 7.0.*
>
> *Professor, this demonstrates a complete, transparent, and academically sound algorithmic trading lifecycle—from natural language to causal AI execution. I welcome any questions."*

---

## 3. Anticipated Faculty Questions & Bulletproof Answers

### Q1: "Are these trades communicating with a live broker or exchange API?"
> **Answer:** *"No, Professor. To maintain strict academic safety and zero financial risk under BCSE418L, this is an authentic Paper Trading Simulator. All order matching, brokerage fee deductions (0.05%), and slippage simulations (0.05%) are executed strictly by our custom `PaperBroker` engine. We have verified through automated regression tests that zero network calls are made to external broker APIs."*

### Q2: "How do you guarantee there is no lookahead bias during playback?"
> **Answer:** *"The historical dataset is ingested into an indexed time-series array, and `AutopilotSession.step()` processes bars sequentially using pointer index $t$. The indicators for candle $t$ are derived exclusively from historical values up to bar $t$. The decision engine evaluates rules using only $t-1$ and $t$ with zero knowledge of bar $t+1$."*

### Q3: "Why not just show a final backtest equity curve instead of a continuous simulator?"
> **Answer:** *"A static backtest equity curve hides path dependency and execution psychology. In live algorithmic trading, an engineer must observe how the system handles whipsaws, whether stop-losses are respected in real time, and why the model chooses to HOLD during sideways consolidation. Autopilot exposes the continuous operational heartbeat of the algorithm."*

### Q4: "How do SHAP and LIME fit into an execution engine?"
> **Answer:** *"Whenever a simulated order is submitted, our backend takes the exact feature vector at that timestamp (close, EMA fast, EMA slow, RSI, volume, ATR) and runs it through both TreeExplainer (for XGBoost) and KernelExplainer/LIME (for PyTorch MLP). This provides verifiable mathematical attribution of which specific market features drove the model's recommendation on that exact day."*

### Q5: "What prevents virtual cash from leaking or drifting across steps?"
> **Answer:** *"We enforce double-entry cash conservation at every step. Total Portfolio Value is strictly computed as Available Cash plus the current marked-to-market value of all open positions. On buys, cash decreases by gross cost plus fees while invested value increases by gross cost. On sells, cash increases by proceeds minus fees. Automated test Step 8 verifies this invariant mathematically to within 1 paisa."*

### Q6: "Can you demonstrate how the system performs under extreme stress or synthetic market shocks?"
> **Answer:** *"Yes! In the top navigation dropdown, we can select **Scenario B: Risk Management** to observe automated stop-loss defense under high volatility, or switch to the **Synthetic Market Sandbox** where we generate clean stochastic Brownian motion with controllable drift to verify model performance independent of historical noise."*
