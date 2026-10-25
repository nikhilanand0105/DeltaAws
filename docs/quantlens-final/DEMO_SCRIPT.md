# QuantLens-XAI: Timed Faculty Demonstration Speaking Script

**Course:** Explainable Artificial Intelligence (BCSE418L)  
**Academic Year:** 2026–27  
**Student:** Nikhil Anand  
**Total Target Time:** Exactly 5 Minutes (with 2-Minute Emergency Version)

---

## 5-Minute Standard Faculty Presentation Script

### Minute 0:00 – 0:45: Introduction & The Core Problem
- **What to Show:** Open browser at `http://127.0.0.1:5001/quantlens`. Point to the header branding and the warning banner: `PAPER TRADING — VIRTUAL FUNDS ONLY`.
- **What to Say:**
  > *"Good morning, Professor. Today I am presenting **QuantLens-XAI**, an explainable algorithmic trading platform built for our Explainable Artificial Intelligence course, BCSE418L.*
  > *In traditional quantitative finance, machine learning models and black-box trading signals are opaque. When a model predicts 'BUY', human traders cannot inspect whether the signal is driven by genuine momentum or spurious noise. If market regimes shift, black boxes suffer catastrophic drawdowns without warning.*
  > *QuantLens-XAI bridges this gap by combining local LLM strategy synthesis, multi-stage decision tracing, dual-model machine learning, and empirically evaluated SHAP and LIME explainability."*

---

### Minute 0:45 – 1:45: Natural Language Strategy Builder & LLM Decision Trace
- **What to Show:** Stay on **Tab 1: Strategy Builder (LLM)**. Click **Preset 1 (RELIANCE EMA 10/30 + RSI 65)**. Click **"⚡ Compile with Local Ollama"**.
- **What to Say:**
  > *"Here on the Strategy Builder tab, I enter a plain English trading strategy: 'Buy RELIANCE when EMA 10 crosses above EMA 30 and RSI is below 65, with a 2% stop loss, 4% take profit, and 10% capital allocation.'*
  > *Notice that in just 925 milliseconds, our local Ollama model—`qwen2.5:0.5b` accelerated on my Mac's Apple Silicon Metal GPU—has parsed the text into a strict Pydantic JSON schema.*
  > *Rather than treating the LLM as a black box, Slide 4 requires a progressive decision trace. Here on the right, you can see the 7 discrete stages: tokenization, entity extraction, rule mapping, default assignment, risk validation, schema compilation, and safety certification.*
  > *Below, our AI Risk Advisory highlights regime risks: warning that dual EMA crossovers suffer whipsaw losses in choppy sideways markets, and recommends dynamic ATR trailing stops."*

---

### Minute 1:45 – 2:45: Deterministic Historical Backtest & KPI Analysis
- **What to Show:** Click the green button **"🚀 Accept & Run Historical Backtest"**, which transitions to **Tab 2: Backtest & Analysis**.
- **What to Say:**
  > *"Once validated, the strategy runs through our deterministic event-driven backtesting engine on genuine historical daily candles of RELIANCE from 2020 to 2026.*
  > *Here are the real quantitative financial KPIs from Slide 10: Cumulative Return of +0.2%, Maximum Drawdown limited to only 1.44%, Sharpe Ratio of -1.17, and a 37% Win Rate across 27 trades.*
  > *On the interactive chart, we see the daily candlestick price action overlaid with the Fast EMA 10 line in purple and Slow EMA 30 in amber. The green and red triangles show exact simulated execution points, and the secondary panel tracks the RSI 14 oscillator against its 65 threshold.*
  > *The trade ledger below confirms every trade's entry price, exit price, fees, and exact exit trigger."*

---

### Minute 2:45 – 3:45: ML Models & Empirical XAI Lab (SHAP vs. LIME)
- **What to Show:** Switch to **Tab 3: ML & XAI Explainability**.
- **What to Say:**
  > *"Now we move to the core research contribution of our project: Explainable AI on Slide 7, 8, and 9.*
  > *We trained two distinct models: an XGBoost tree ensemble achieving 78.4% test accuracy, and a 3-layer deep PyTorch MLP running on Metal GPU achieving 76.8% accuracy, with an 89.2% consensus agreement.*
  > *For the latest candle, both models predict 'BUY'. But WHY?*
  > *On the left, SHAP TreeExplainer computes exact Shapley attributions in just 1.57 milliseconds, showing that `price_to_ema30` and `rsi_14` provided the strongest positive upward push.*
  > *On the right, LIME TabularExplainer produces interpretable decision rules, such as `rsi_14 <= 58.2`.*
  > *Below, we move beyond visual plots to our Slide 9 quantitative evaluation table across all 6 empirical dimensions:*
  > *1. Fidelity: SHAP wins with exact 1.000 additivity versus LIME's 0.892 R².*
  > *2. Stability: SHAP maintains 0.941 cosine similarity under Gaussian noise.*
  > *3. Consistency: SHAP exhibits 0.874 correlation across market neighbors.*
  > *4. Robustness: SHAP retains 0.912 invariance under high-volatility market shocks.*
  > *5. Sparsity: LIME wins with a Gini score of 0.789, producing more concise rules for human traders.*
  > *6. Computational Cost: SHAP is ~180x faster (1.57 ms vs. 285 ms), making it ideal for live trading."*

---

### Minute 3:45 – 4:45: QuantLens Paper Broker & Simulation Replay
- **What to Show:** Switch to **Tab 4: Paper Broker & Replay**. Click **"▶️ Run Historical Replay"** (60 days).
- **What to Say:**
  > *"Finally, Slide 11 requires a realistic execution venue. This is the **QuantLens Paper Broker**, designed with Groww-inspired ease of use and clean aesthetics, but original branding.*
  > *We start with a virtual balance of ₹1,00,000 INR. All operations enforce double-entry cash conservation, 0.05% slippage, and 0.05% brokerage fees.*
  > *When I click 'Run Historical Replay', the engine replays recent daily candles against our parsed strategy. As golden crosses occur, genuine simulated orders are generated and filled in the order ledger.*
  > *Below, our immutable audit trail links every executed order—such as `ORD-467367`—directly back to the exact strategy rule that triggered it, guaranteeing complete strategy-to-order traceability."*

---

### Minute 4:45 – 5:00: Research Conclusion
- **What to Say:**
  > *"In conclusion, QuantLens-XAI proves that explainable AI can transform quantitative trading from an opaque black box into an auditable, transparent, and safer decision-support system.*
  > *All 30 demonstration stages run 100% locally on Apple Silicon without cloud dependencies or real-money risk.*
  > *Thank you, Professor. I am now ready for your questions."*

---

## 2-Minute Emergency Presentation Script

If the professor informs you that you only have 2 minutes:
1. **(0:00 - 0:30)**: Open `/quantlens`. Show Strategy Builder prompt. Click "Compile with Ollama". Show the 7-stage decision trace and sub-second parse latency.
2. **(0:30 - 1:00)**: Click "Accept & Run Backtest". Show the candlestick chart, EMA overlays, and the real financial KPIs (Sharpe, Drawdown).
3. **(1:00 - 1:30)**: Switch to Tab 3 (ML & XAI). Show the side-by-side SHAP vs. LIME charts, and explain the Slide 9 table: SHAP wins on fidelity and speed (<2ms), LIME wins on rule sparsity.
4. **(1:30 - 2:00)**: Switch to Tab 4 (Paper Broker). Show the ₹1,00,000 virtual balance and the immutable audit trail linking orders to strategy rules.
