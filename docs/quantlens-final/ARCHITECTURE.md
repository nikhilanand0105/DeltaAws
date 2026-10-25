# QuantLens-XAI: Technical Architecture & System Design Document

**Course:** Explainable Artificial Intelligence (BCSE418L)  
**Academic Year:** 2026–27  
**Student:** Nikhil Anand  
**System Version:** 2.0 (Academic Release)

---

## 1. Architectural Philosophy

QuantLens-XAI is designed around five core architectural tenets:
1. **Explainability First**: Every trading signal, machine learning inference, and strategy parameter must be accompanied by an interpretable explanation (local feature attributions, surrogate rules, or mathematical indicator rationale).
2. **Deterministic Reproducibility**: Given the same historical dataset and strategy prompt, backtests and simulations yield 100% identical financial metrics.
3. **Zero Future-Data Leakage**: All technical indicators, scalers, and time-series splits strictly respect causality.
4. **Local Hardware Acceleration**: Leveraging Apple Silicon M1 Pro unified memory architecture with Metal GPU compute for both Ollama LLM inference and PyTorch deep neural network forward passes.
5. **Double-Entry Financial Conservation**: The paper broker maintains strict conservation of capital: $\text{Cash} + \text{Invested Market Value} = \text{Total Portfolio Value}$, with transparent accounting for slippage and brokerage turnover fees.

---

## 2. Layered Architecture

```
+-----------------------------------------------------------------------------------+
|                            PRESENTATION LAYER                                     |
|  - QuantLens-XAI Unified Web App (templates/quantlens.html)                       |
|  - Tab 1: Natural Language Strategy Builder & 7-Stage Decision Trace              |
|  - Tab 2: Strategy Backtest & Candlestick Analysis (ApexCharts)                   |
|  - Tab 3: Machine Learning & XAI Explainability Lab (SHAP / LIME / Slide 9)      |
|  - Tab 4: QuantLens Paper Broker (Groww-inspired UI & Historical Replay)          |
+-----------------------------------------------------------------------------------+
                                        | (REST JSON APIs)
+-----------------------------------------------------------------------------------+
|                        APPLICATION & ROUTING LAYER                                |
|  - Flask Application (app.py) & Blueprint (quantlens/routes.py)                   |
|  - /api/quantlens/parse-strategy      | /api/quantlens/validate-strategy          |
|  - /api/quantlens/backtest            | /api/quantlens/xai-explain                |
|  - /api/quantlens/paper-broker/*      | /api/quantlens/models/status              |
+-----------------------------------------------------------------------------------+
                                        |
+-----------------------------------------------------------------------------------+
|                         QUANTLENS CORE ENGINE LAYER                               |
|  - LLM Strategy Parser: quantlens/llm_parser.py (Ollama qwen2.5:0.5b)             |
|  - Schema & Validator: quantlens/strategy_schema.py, strategy_validator.py       |
|  - Backtesting Engine: quantlens/backtest_engine.py (Event-driven KPIs)           |
|  - Simulation Engine: quantlens/simulation_engine.py (Historical candle replay)   |
|  - Paper Broker Engine: quantlens/paper_broker.py (₹1,00,000 virtual ledger)      |
+-----------------------------------------------------------------------------------+
                                        |
+-----------------------------------------------------------------------------------+
|                     MACHINE LEARNING & XAI RESEARCH LAYER                         |
|  - Feature Engineering: quantlens/feature_engineering.py (22 Causal Indicators)   |
|  - Model Manager: quantlens/ml_models.py (XGBoost + PyTorch MPS Metal MLP)        |
|  - XAI Engine: quantlens/xai_engine.py (SHAP TreeExplainer & LIME Tabular)        |
|  - XAI Evaluator: quantlens/xai_evaluation.py (Slide 9: 6 Quantitative Metrics)   |
+-----------------------------------------------------------------------------------+
                                        |
+-----------------------------------------------------------------------------------+
|                             DATA & PERSISTENCE LAYER                              |
|  - Offline Daily OHLCV Storage: data/historical/*.csv (RELIANCE, TCS, INFY, NIFTY)|
|  - Pretrained Model Weights: models/xgboost_*.json, models/pytorch_*.pt           |
|  - Paper Broker State: data/paper_broker_state.json                               |
|  - Empirical Benchmark Cache: cache/xai/reliance_xai_cache.json                   |
+-----------------------------------------------------------------------------------+
```

---

## 3. Component Details

### 3.1 LLM Strategy Parser (`quantlens/llm_parser.py`)
- Communicates over local HTTP socket `http://127.0.0.1:11434/api/generate` with `"format": "json"`.
- Uses system instructions constraining the LLM to extract only valid numerical parameters (EMA periods, RSI threshold, Stop Loss %, Take Profit %, capital allocation).
- Generates 7-step visual decision trace and educational risk analysis.
- Guaranteed deterministic fallback if Ollama daemon is offline.

### 3.2 Strategy Validation & Schema (`quantlens/strategy_schema.py`, `quantlens/strategy_validator.py`)
- Pydantic v2 schemas: `StrategyDefinition`, `IndicatorConfig`, `EntryRule`, `ExitRule`, `RiskManagement`.
- Enforces financial sanity rules: Fast EMA strictly less than Slow EMA, SL > 0, TP > 0, maximum allocation $\le 100\%$, supported symbol universe.

### 3.3 Event-Driven Backtesting Engine (`quantlens/backtest_engine.py`)
- Deterministic simulation of cash and position state over time.
- Calculates standard financial metrics:
  $$\text{Sharpe Ratio} = \sqrt{252} \times \frac{\mu_r - r_f}{\sigma_r}$$
  $$\text{Sortino Ratio} = \sqrt{252} \times \frac{\mu_r - r_f}{\sigma_{d}}$$
  $$\text{Maximum Drawdown} = \max_{t} \left( \frac{\text{Peak}_t - \text{Equity}_t}{\text{Peak}_t} \right)$$
  $$\text{Profit Factor} = \frac{\sum \text{Gross Profits}}{\sum \text{Gross Losses}}$$

### 3.4 Multi-Model ML & XAI Engine (`quantlens/ml_models.py`, `quantlens/xai_engine.py`, `quantlens/xai_evaluation.py`)
- Computes 22 causal indicators.
- Chronological time-series split (70% train, 15% validation, 15% test).
- Dual model architecture:
  - **XGBoost**: Tree ensemble trained with `multi:softprob` across 3 classes.
  - **PyTorch MLP**: Deep neural network with Linear, BatchNorm1d, ReLU, Dropout, and Softmax layers accelerated on Apple Metal GPU (`mps`).
- **SHAP TreeExplainer**: Fast C++ polynomial calculation of exact additive Shapley feature attributions.
- **LIME TabularExplainer**: Local weighted ridge regression surrogate explaining individual bars with bounded interval decision rules.
- **Slide 9 Evaluation Suite**: Evaluates Fidelity, Stability, Consistency, Robustness, Sparsity, and Computational Cost.

### 3.5 Paper Broker & Simulation Replay (`quantlens/paper_broker.py`, `quantlens/simulation_engine.py`)
- Virtual cash account initialized to ₹1,00,000 INR.
- Slippage model: $+0.05\%$ on BUY, $-0.05\%$ on SELL.
- Brokerage fee: $0.05\%$ on gross order value.
- Strategy-to-order traceability: Every order records the generating rule reason and links to an immutable audit record (`AUD-XXXX`).
