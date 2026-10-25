# QuantLens-XAI: End-to-End Data Flow Architecture

## 1. System Overview
QuantLens-XAI operates as a closed-loop quantitative pipeline connecting natural language inputs to validated strategy schemas, backtesting simulations, dual ML model inference, SHAP/LIME explainability, and paper execution.

```
[ User Natural Language Prompt ]
               |
               v
   [ Local Ollama LLM Parser ]  ---> (Pydantic v2 Schema Validation)
               |
               v
  [ 7-Stage Visual Decision Trace ] + [ AI Risk Advisory ]
               |
               v
    [ Event-Driven Backtest ]  <--- (Historical OHLCV CSVs)
               |
               v
   [ Dual ML Inference Pipeline ]
      |                      |
      v                      v
[ XGBoost Classifier ]  [ PyTorch Metal MLP ]
      |                      |
      +----------+-----------+
                 |
                 v
   [ Real XAI Attribution Engine ]
      |                      |
      v                      v
[ SHAP TreeExplainer ]  [ LIME TabularExplainer ]
                 |
                 v
   [ Slide 9 Empirical Evaluation ]
                 |
                 v
   [ Groww-Inspired Paper Broker ]
        |                   |
        v                   v
 [ SQLite: Config/Auth ] [ MongoDB: Orders/Positions/Audits ]
```

---

## 2. Pipeline Stages

### Stage 1: Natural Language Strategy Parsing
1. User provides prompt: *"Buy RELIANCE when EMA 10 crosses above EMA 30 and RSI is below 65, exit on reverse crossover or 2% stop loss, 4% take profit with 10% max capital allocation."*
2. Prompt is dispatched to local Ollama runtime (`qwen2.5:0.5b`) via HTTP POST on `http://127.0.0.1:11434/api/generate`.
3. LLM returns JSON schema matching Pydantic model `TradingStrategySchema`.
4. System computes latency ($\approx 1,000\text{ ms}$) and renders the 7-stage visual decision trace.

### Stage 2: Strategy Backtesting & Indicator Generation
1. Historical daily OHLCV dataset (`data/historical/RELIANCE.csv`) is loaded via pandas.
2. Exponential Moving Averages (EMA 10, EMA 30) and Relative Strength Index (RSI 14) are computed.
3. Event-driven simulator models realistic slippage ($0.05\%$) and transaction fees ($₹15/\text{trade}$).
4. Metrics calculated: Cumulative Return, Sharpe Ratio, Sortino Ratio, Maximum Drawdown, Win Rate, and Profit Factor.

### Stage 3: Dual Machine Learning Inference
1. Feature vector extracted from latest market state (Normalized EMA ratio, RSI, MACD, Volume momentum, Volatility).
2. XGBoost model (`models/xgboost_reliance.json`) executes inference on CPU.
3. PyTorch Deep Neural Network (`models/pytorch_reliance.pt`) executes inference on Apple Silicon Metal Performance Shaders (MPS / CPU fallback).
4. Dual predictions generate confidence probabilities for directional movement.

### Stage 4: Explainable AI (XAI) Attribution
1. **SHAP TreeExplainer**: Evaluates Shapley values $\phi_i$ across all features, guaranteeing efficiency and additivity ($\sum \phi_i = f(x) - \mathbb{E}[f(x)]$).
2. **LIME TabularExplainer**: Fits local linear surrogate model $g \in G$ minimizing $\mathcal{L}(f, g, \pi_x) + \Omega(g)$ with exponential kernel weighting.
3. Slide 9 Empirical Benchmarks computed across 6 dimensions: Fidelity, Stability, Consistency, Robustness, Sparsity, and Cost (latency).
4. Explanations stored in MongoDB `xai_explanations` and `xai_evaluation_results`.

### Stage 5: Paper Broker Execution & Double-Entry Accounting
1. Validated trade signals generate orders with IDs `ORD-YYYYMMDD-XXXX`.
2. Available cash checked; capital deducted with fee recording.
3. Position created or updated in MongoDB `paper_positions`.
4. Tamper-evident audit event recorded in MongoDB `paper_audit_events`.
