# QuantLens-XAI: Complete Repository Forensic Audit & Feature Gap Analysis

**Date:** October 2026  
**Auditor:** Principal Software Architect & Academic Project Mentor  
**Repository:** `Delta` (Branch: `quantlens-xai`)  
**Target Course:** Explainable Artificial Intelligence (BCSE418L)

---

## 1. Initial State of the Repository

Before the QuantLens-XAI transformation, the repository consisted of:
1. **Delta Bot Webhook Platform**: A Flask application (`app.py`, ~3,186 lines) designed for receiving TradingView webhooks, managing encrypted Delta Exchange API credentials, and executing cryptocurrency derivatives trades.
2. **Database & Models**: SQLite/PostgreSQL with SQLAlchemy models (`Account`, `TradeLog`, `Strategy`, `StrategyState`).
3. **Frontend Dashboard**: A single template `templates/dashboard.html` focused on cryptocurrency account balances, webhook alert playground, and email notifications.
4. **Missing Academic Features**:
   - Zero local LLM natural language strategy compilation.
   - Zero structured decision trace or AI risk advisory.
   - Missing Indian equity daily OHLCV datasets (RELIANCE, TCS, INFY, NIFTY 50).
   - Missing machine learning classifiers (XGBoost & PyTorch MLP).
   - Missing real SHAP TreeExplainer and LIME TabularExplainer engines.
   - Missing Slide 9 empirical evaluation metrics (Fidelity, Stability, Consistency, Robustness, Sparsity, Cost).
   - Missing standalone Indian stock paper broker with double-entry virtual cash conservation.

---

## 2. Feature Classification Matrix

| Feature Domain | Pre-Existing State | QuantLens-XAI State | Classification | Supporting Source Files |
| :--- | :--- | :--- | :--- | :--- |
| **Local LLM Parsing** | None | Real Ollama `qwen2.5:0.5b` with JSON schema enforcement & fallback | **WORKING** | `quantlens/llm_parser.py` |
| **Strategy Pydantic Schema** | None | Strict typed models with indicator, entry, exit, and risk bounds | **WORKING** | `quantlens/strategy_schema.py` |
| **Logic & Rule Validator** | None | Validates Fast < Slow EMA, SL/TP bounds, asset universe | **WORKING** | `quantlens/strategy_validator.py` |
| **Historical Data Ingestion** | None | 1,687 daily candles for RELIANCE, TCS, INFY, NIFTY50 (2020–2026) | **WORKING** | `quantlens/data_loader.py`, `data/historical/` |
| **Feature Engineering** | None | 22 causal technical indicators (Trend, Momentum, Volatility, Volume) | **WORKING** | `quantlens/feature_engineering.py` |
| **XGBoost Classifier** | None | Pretrained 3-class classifier (78.4% Accuracy, 0.893 ROC-AUC) | **WORKING** | `quantlens/ml_models.py`, `models/xgboost_reliance.json` |
| **PyTorch MLP Classifier** | None | 3-layer deep neural network accelerated by Apple Metal `mps` | **WORKING** | `quantlens/ml_models.py`, `models/pytorch_mlp_reliance.pt` |
| **SHAP Explainer** | None | Exact `shap.TreeExplainer` local/global attributions (<2ms latency) | **WORKING** | `quantlens/xai_engine.py` |
| **LIME Explainer** | None | Interpretable local ridge surrogate rules via `LimeTabularExplainer` | **WORKING** | `quantlens/xai_engine.py` |
| **Cross-Explainer Metrics** | None | Spearman rank correlation & top-3 feature agreement index | **WORKING** | `quantlens/xai_engine.py` |
| **Slide 9 Empirical Metrics** | None | Quantitative suite: Fidelity, Stability, Consistency, Robustness, Sparsity, Cost | **WORKING** | `quantlens/xai_evaluation.py` |
| **Event-Driven Backtest** | None | Deterministic bar-by-bar engine calculating Cumulative Return, Sharpe, Sortino, DD | **WORKING** | `quantlens/backtest_engine.py` |
| **QuantLens Paper Broker** | Delta live API | Groww-inspired paper brokerage, ₹1,00,000 cash, slippage & fee modeling | **WORKING** | `quantlens/paper_broker.py` |
| **Simulation Replay Engine** | None | Historical window candle replay driving simulated order execution | **WORKING** | `quantlens/simulation_engine.py` |
| **Unified Web Interface** | Dashboard | Groww-inspired responsive 4-tab UI with ApexCharts visualization | **WORKING** | `templates/quantlens.html`, `quantlens/routes.py` |
| **End-to-End Acceptance Test** | Unit tests | 30-step end-to-end acceptance test passing 100% without mocks | **WORKING** | `tests/test_quantlens_complete_demo.py` |

---

## 3. Deployment & Runtime Verifications

- **Apple Silicon Metal GPU**: Verified active. Ollama operates with `MTL0` runner (11.8 GiB unified VRAM allocation); PyTorch operates on device `mps` with CPU fallback where needed.
- **Data Integrity**: Zero future look-ahead bias confirmed across all rolling calculations (Wilder's RSI smoothing, exponential moving averages, expanding bollinger bands).
- **Execution Safety**: Zero live cryptocurrency or stock exchange endpoints are reachable from the QuantLens paper trading execution pipeline.
