# QuantLens-XAI: Research Presentation Requirement Compliance Matrix

**Reference Document:** `QuantLens-XAI (1).pdf` (12 Research Proposal Slides)  
**Course:** Explainable Artificial Intelligence (BCSE418L)  
**Academic Year:** 2026–27  
**Student:** Nikhil Anand

---

## Slide-by-Slide Requirement Traceability

| Slide | Slide Title & Core Topic | PPT Requirements & Methodologies | QuantLens Implementation Module | Verification Status |
| :--- | :--- | :--- | :--- | :--- |
| **Slide 1** | Title Slide | QuantLens-XAI: Explainable Algorithmic Trading Platform | `templates/quantlens.html`, `quantlens/__init__.py` | **100% IMPLEMENTED** |
| **Slide 2** | Introduction & Problem Statement | Black-box financial predictions, opaque algorithmic signals, risk of unexplained catastrophic losses, need for human-in-the-loop decision support | `quantlens/llm_parser.py`, `quantlens/strategy_schema.py` | **100% IMPLEMENTED** |
| **Slide 3** | System Architecture | End-to-end pipeline: NL strategy -> Local LLM -> Schema Validation -> Decision Trace -> Backtesting -> Multi-Model Inference -> XAI Attribution -> Paper Execution | `quantlens/routes.py`, `templates/quantlens.html` | **100% IMPLEMENTED** |
| **Slide 4** | Research Workflow & Decision Process | 7-stage progressive decision trace: Tokenization, Entity extraction, Rule synthesis, Risk boundary check, Fallback assignment, Schema compilation, Readiness check | `quantlens/llm_parser.py` (`generate_decision_trace`), `quantlens/strategy_schema.py` | **100% IMPLEMENTED** |
| **Slide 5** | Data Acquisition & Provenance | Daily OHLCV data for Indian equities (RELIANCE, TCS, INFY, NIFTY 50), 2020–2026, offline CSV storage, zero future leakage | `quantlens/data_loader.py`, `data/historical/*.csv` | **100% IMPLEMENTED** |
| **Slide 6** | Feature Engineering & Indicators | 22 causal technical indicators: SMA (10, 30, 50), EMA (10, 20, 30, 50), RSI(14), MACD(12,26,9), Bollinger Bands(20,2), ATR(14), OBV, Volume ratios | `quantlens/feature_engineering.py` | **100% IMPLEMENTED** |
| **Slide 7** | Machine Learning & Deep Learning Models | Multi-class prediction: BUY [2], HOLD [1], SELL [0]. Gradient Boosted Trees (XGBoost) and Deep Neural Network (PyTorch MLP on Apple Metal MPS) | `quantlens/ml_models.py`, `models/xgboost_reliance.json`, `models/pytorch_mlp_reliance.pt` | **100% IMPLEMENTED** |
| **Slide 8** | Explainable AI (XAI) Methods | Dual explainer suite: SHAP TreeExplainer (exact polynomial Shapley values) & LIME TabularExplainer (local linear surrogate rules) | `quantlens/xai_engine.py` | **100% IMPLEMENTED** |
| **Slide 9** | Explanation Quality Evaluation | Quantitative 6-metric benchmarking suite: Fidelity (R²/Additivity), Stability (Lipschitz Gaussian noise), Consistency (Spearman rank), Robustness (ATR volatility), Sparsity (Gini coefficient), Computational Cost (ms) | `quantlens/xai_evaluation.py` | **100% IMPLEMENTED** |
| **Slide 10** | Quantitative Strategy Backtesting | Deterministic event-driven backtesting engine calculating: Cumulative Return, Sharpe Ratio, Sortino Ratio, Maximum Drawdown, Win Rate, Profit Factor, interactive candlestick & marker overlays | `quantlens/backtest_engine.py` | **100% IMPLEMENTED** |
| **Slide 11** | Research Interface & Paper Broker | Groww-inspired paper trading interface, virtual ₹1,00,000 cash, order ledger, open positions, double-entry cash conservation, slippage/fee modeling, strategy-to-order audit log | `quantlens/paper_broker.py`, `quantlens/simulation_engine.py`, `templates/quantlens.html` | **100% IMPLEMENTED** |
| **Slide 12** | Conclusion & Research Contributions | Bridge between black-box AI and quantitative trading; demonstrated that SHAP achieves superior fidelity and speed (<5ms) while LIME excels in rule sparsity; fully reproducible offline academic pipeline | `docs/quantlens-final/PERFORMANCE_REPORT.md`, `tests/test_quantlens_complete_demo.py` | **100% IMPLEMENTED** |

---

## Summary of Verification
Every single mathematical formula, predictive model, indicator, XAI method, evaluation metric, and UI component from all 12 slides of the research presentation is implemented in genuine Python and JavaScript code, verified against real historical Indian stock market data, and exercised by `tests/test_quantlens_complete_demo.py`.
