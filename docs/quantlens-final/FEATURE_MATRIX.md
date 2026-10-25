# QuantLens-XAI: Feature & Requirement Traceability Matrix

## 1. Compliance Matrix

| Requirement ID | PPT / Rubric Feature Description | Implementation Module | Verification Status |
| :--- | :--- | :--- | :--- |
| **REQ-01** | Natural Language Trading Strategy Generation | `quantlens/llm_parser.py` (Ollama `qwen2.5:0.5b`) | Fully Verified (Step 2) |
| **REQ-02** | Structured JSON Strategy Schema Validation | `quantlens/schema.py` (Pydantic v2) | Fully Verified (Step 4) |
| **REQ-03** | 7-Stage Visual Decision Trace & AI Advisory | `templates/quantlens.html` & `quantlens/llm_parser.py` | Fully Verified (Step 6) |
| **REQ-04** | Event-Driven Backtesting with Candlestick & Indicators | `quantlens/backtest_engine.py` (ApexCharts) | Fully Verified (Step 9) |
| **REQ-05** | Dual Machine Learning Models (XGBoost + PyTorch) | `quantlens/ml_models.py` (CPU + Metal MPS) | Fully Verified (Step 13) |
| **REQ-06** | Real Explainable AI Attributions (SHAP + LIME) | `quantlens/xai_engine.py` (TreeExplainer + LIME) | Fully Verified (Step 16) |
| **REQ-07** | Slide 9 Empirical XAI Evaluation Framework | `quantlens/xai_evaluation.py` (6 metrics) | Fully Verified (Step 19) |
| **REQ-08** | Groww-Inspired Paper Broker with ₹10L Virtual Capital | `quantlens/paper_broker.py` (MongoDB) | Fully Verified (Step 22) |
| **REQ-09** | Double-Entry Accounting & Immutable Audit Trail | `quantlens/paper_broker.py` (`paper_audit_events`) | Fully Verified (Step 25) |
| **REQ-10** | Hybrid Database Architecture (SQLite + MongoDB 7.0) | `quantlens/db_mongodb.py` & `models.py` | Fully Verified (Step 28) |
