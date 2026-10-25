# QuantLens-XAI: Known Limitations, Assumptions & Future Research Directions

**Course:** Explainable Artificial Intelligence (BCSE418L)  
**Academic Year:** 2026–27  
**Student:** Nikhil Anand

---

## 1. Academic Honesty Statement

In accordance with Section 22 and Section 23 of the course project guidelines, we present an honest technical disclosure of current limitations, assumptions, and future enhancements rather than claiming the system is without boundaries.

---

## 2. Technical Limitations & Constraints

### 2.1 Daily OHLCV Resolution vs. Intraday Tick Dynamics
- **Current Scope:** The platform operates on daily candlestick bars (1D resolution).
- **Limitation:** Intraday volatility spikes, order-book depth dynamics (Level-2 bid/ask queues), and sub-minute execution queuing are not modeled.
- **Future Direction:** Ingest 1-minute or 5-minute intraday bars via websocket streams for high-frequency algorithmic research.

### 2.2 Local LLM Parameter Extraction Complexity
- **Current Scope:** Operates on lightweight 0.5B to 4B local LLMs (`qwen2.5:0.5b`).
- **Limitation:** Highly convoluted natural language prompts containing nested conditional logic (e.g. *"Buy if 50 SMA crosses 200 SMA on daily, but only if 15-minute Stochastic oscillator was oversold 2 bars ago and open interest rose 5%"*) can exceed the single-pass reasoning capacity of small quantized models, requiring fallback to default assumption handling.
- **Future Direction:** Implement multi-step chain-of-thought prompting with iterative JSON schema refinement.

### 2.3 LIME Sampling Latency
- **Current Scope:** `LimeTabularExplainer` generates 5,000 neighborhood perturbations per sample.
- **Limitation:** While SHAP TreeExplainer computes attributions in ~1.57 ms, LIME requires ~285 ms. While entirely acceptable for daily decision support, 285 ms is too slow for sub-second high-frequency execution.
- **Future Direction:** Implement parallelized surrogate sampling via GPU compute shaders or C++ bindings.

### 2.4 Stationary Time-Series Assumption
- **Current Scope:** Technical indicators assume non-stationary price series can be normalized into stationary momentum and ratio features (`rsi_14`, `price_to_ema30`).
- **Limitation:** Extreme structural breaks (e.g., pandemic market crashes or macroeconomic policy shocks) alter distribution regimes in ways that fixed-window rolling indicators cannot anticipate.
- **Future Direction:** Incorporate hidden Markov models (HMM) or Gaussian Mixture Models (GMM) for explicit probabilistic market regime classification.

---

## 3. Financial Safety Disclaimers

1. **Virtual Simulation Only**: All balances, trades, and ledgers in QuantLens-XAI represent simulated paper capital.
2. **Not Financial Advice**: Past backtested performance is not indicative of future market returns. The system is designed strictly for academic evaluation under VIT's BCSE418L course curriculum.
