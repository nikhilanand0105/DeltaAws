# QuantLens-XAI: REST API Reference Manual

## 1. Base URL
All QuantLens-XAI REST endpoints are served on:
```
http://127.0.0.1:5001/api/quantlens
```

---

## 2. API Endpoint Directory

| Method | Endpoint | Description | Storage Backend |
| :--- | :--- | :--- | :--- |
| `POST` | `/parse-strategy` | Parses natural language prompt via local Ollama LLM into validated strategy schema | In-Memory / Pydantic |
| `POST` | `/backtest` | Executes event-driven backtesting on historical stock datasets | In-Memory / File CSV |
| `GET` | `/xai-explanation` | Retrieves SHAP & LIME local feature attributions and ML inference | MongoDB (`xai_explanations`) |
| `GET` | `/xai-evaluation` | Retrieves Slide 9 empirical evaluation metrics across 6 dimensions | MongoDB (`xai_evaluation_results`) |
| `GET` | `/paper-account` | Retrieves virtual portfolio balance, active positions, and open orders | MongoDB (`paper_accounts`, `paper_positions`, `paper_orders`) |
| `POST` | `/paper-order` | Submits a manual paper trade order with double-entry accounting | MongoDB (`paper_orders`, `paper_audit_events`) |
| `POST` | `/paper-reset` | Resets paper broker state to ₹10,00,000 virtual cash and zero positions | MongoDB Collections Reset |
| `POST` | `/paper-simulation-replay` | Executes historical simulation replay with parameter sweep | MongoDB (`paper_simulation_runs`) |
| `GET` | `/db-status` | Real-time health check for both SQLite 3 and MongoDB 7.0 | SQLite 3 & MongoDB 7.0 |

---

## 3. Endpoint Specifications

### 1. `POST /api/quantlens/parse-strategy`
**Request Payload**:
```json
{
  "prompt": "Buy RELIANCE when EMA 10 crosses above EMA 30 and RSI < 65, stop loss 2%, take profit 4%",
  "symbol": "RELIANCE"
}
```
**Response (200 OK)**:
```json
{
  "success": true,
  "data": {
    "strategy": {
      "strategy_id": "strat-20261025-01",
      "symbol": "RELIANCE",
      "timeframe": "1d",
      "entry_rules": [{"indicator": "EMA", "period": 10, "condition": "crosses_above", "target": "EMA_30"}],
      "exit_rules": [{"indicator": "EMA", "period": 10, "condition": "crosses_below", "target": "EMA_30"}],
      "risk_management": {"stop_loss_pct": 2.0, "take_profit_pct": 4.0, "max_capital_allocation_pct": 10.0}
    },
    "decision_trace": [
      {"stage": 1, "name": "Natural Language Input", "status": "COMPLETED"},
      {"stage": 2, "name": "LLM Tokenization & Intent Extraction", "status": "COMPLETED"},
      {"stage": 3, "name": "Pydantic Schema Validation", "status": "COMPLETED"},
      {"stage": 4, "name": "Technical Indicator Alignment", "status": "COMPLETED"},
      {"stage": 5, "name": "Risk Boundary Verification", "status": "COMPLETED"},
      {"stage": 6, "name": "Execution Feasibility Check", "status": "COMPLETED"},
      {"stage": 7, "name": "AI Advisory Formulation", "status": "COMPLETED"}
    ],
    "advisory": {
      "confidence_score": 0.88,
      "risk_level": "MODERATE",
      "summary": "Strategy displays balanced risk-reward with well-defined exit boundaries."
    },
    "execution_time_ms": 1042
  }
}
```

### 2. `GET /api/quantlens/db-status`
**Response (200 OK)**:
```json
{
  "success": true,
  "architecture": "Hybrid SQL (SQLite) + NoSQL (MongoDB)",
  "sqlite": {
    "connected": true,
    "engine": "SQLite 3 (via SQLAlchemy 2.0)",
    "file_path": "/Users/nikhilanand/Downloads/Delta/instance/local.db",
    "integrity": "ok",
    "tables": {
      "accounts": 5,
      "settings": 2,
      "strategies": 5,
      "strategy_states": 12,
      "trade_logs": 24,
      "local_signal_logs": 18
    }
  },
  "mongodb": {
    "connected": true,
    "database": "quantlens_xai",
    "server_version": "7.0.41",
    "uri": "mongodb://localhost:27017/",
    "collections": {
      "paper_accounts": 1,
      "paper_positions": 0,
      "paper_orders": 4,
      "paper_trades": 2,
      "paper_audit_events": 5,
      "paper_simulation_runs": 1,
      "xai_explanations": 1,
      "xai_evaluation_results": 1
    }
  }
}
```
