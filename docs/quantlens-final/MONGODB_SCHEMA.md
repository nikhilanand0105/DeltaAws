# QuantLens-XAI: Document Database Schema (MongoDB 7.0)

## 1. Overview
The NoSQL document storage layer is implemented in **MongoDB Community Edition 7.0** under the database **`quantlens_xai`** on `localhost:27017`. It contains 8 specialized collections designed for high-throughput paper trading, simulation replays, and Explainable AI (XAI) attributions.

---

## 2. Collection Directory & Indexing Strategy

| Collection Name | Role | Primary Key / Unique Indexes | Secondary Indexes |
| :--- | :--- | :--- | :--- |
| `paper_accounts` | Virtual Cash, Equity & P&L | `account_id` (Unique) | `trading_mode` |
| `paper_positions` | Open Holdings per Account | `(account_id, symbol)` (Compound Unique) | `symbol` |
| `paper_orders` | Orders Ledger (`ORD-XXXXXX`) | `order_id` (Unique) | `account_id`, `status`, `timestamp` |
| `paper_trades` | Closed Round-Trip Executions | `trade_id` (Unique) | `symbol`, `timestamp` |
| `paper_audit_events` | Immutable Double-Entry Audit | `audit_id` (Unique) | `account_id`, `event_type`, `timestamp` |
| `paper_simulation_runs` | Replay Simulation Runs | `run_id` (Unique) | `symbol`, `timestamp` |
| `xai_explanations` | Local SHAP/LIME Caches | `cache_key` (Unique) | `symbol`, `timestamp` |
| `xai_evaluation_results`| Slide 9 Empirical Benchmarks | `symbol` (Unique) | `timestamp` |

---

## 3. Detailed Collection Schemas (BSON)

### 1. `paper_accounts`
Maintains virtual capital and portfolio equity for the Groww-inspired paper broker.
```json
{
  "_id": ObjectId("..."),
  "account_id": "paper_user_default",
  "initial_capital": 1000000.0,
  "available_cash": 900421.0,
  "realized_pnl": 421.0,
  "trading_mode": "PAPER_TRADING",
  "updated_at": "2026-10-25T13:21:25.801Z"
}
```

### 2. `paper_positions`
Tracks current stock holdings, average acquisition costs, and unrealized gains.
```json
{
  "_id": ObjectId("..."),
  "account_id": "paper_user_default",
  "symbol": "RELIANCE",
  "quantity": 38,
  "average_buy_price": 2620.50,
  "current_market_price": 2628.00,
  "unrealized_pnl": 285.0,
  "updated_at": "2026-10-25T13:21:25.805Z"
}
```

### 3. `paper_orders`
Append-only order book tracking the full lifecycle of buy/sell intents.
```json
{
  "_id": ObjectId("..."),
  "order_id": "ORD-20261025-4921",
  "account_id": "paper_user_default",
  "symbol": "RELIANCE",
  "side": "BUY",
  "quantity": 38,
  "price": 2620.50,
  "order_type": "MARKET",
  "status": "FILLED",
  "total_value": 99579.0,
  "execution_fee": 15.0,
  "idempotency_key": "IDEMP-RELIANCE-1729849285",
  "timestamp": "2026-10-25T13:21:25.801Z"
}
```

### 4. `paper_trades`
Records completed round trips with realized P&L and broker fees.
```json
{
  "_id": ObjectId("..."),
  "trade_id": "TRD-20261025-1029",
  "symbol": "RELIANCE",
  "buy_order_id": "ORD-20261025-4920",
  "sell_order_id": "ORD-20261025-4921",
  "quantity": 38,
  "entry_price": 2605.00,
  "exit_price": 2616.50,
  "realized_pnl": 437.0,
  "net_pnl": 407.0,
  "holding_period_days": 3,
  "timestamp": "2026-10-25T13:21:25.810Z"
}
```

### 5. `paper_audit_events`
Immutable double-entry ledger verifying capital conservation ($\Delta\text{Cash} + \Delta\text{Position} = 0$).
```json
{
  "_id": ObjectId("..."),
  "audit_id": "AUD-20261025-8831",
  "account_id": "paper_user_default",
  "event_type": "ORDER_FILLED",
  "details": {
    "order_id": "ORD-20261025-4921",
    "symbol": "RELIANCE",
    "quantity": 38,
    "cash_deducted": 99579.0
  },
  "timestamp": "2026-10-25T13:21:25.805Z"
}
```

### 6. `paper_simulation_runs`
Records multi-day historical replay simulations and stress tests.
```json
{
  "_id": ObjectId("..."),
  "run_id": "SIM-20261025-3312",
  "symbol": "RELIANCE",
  "start_date": "2023-01-01",
  "end_date": "2024-01-01",
  "total_trades": 14,
  "cumulative_return_pct": 14.85,
  "max_drawdown_pct": 3.42,
  "sharpe_ratio": 1.74,
  "timestamp": "2026-10-25T13:21:25.820Z"
}
```

### 7. `xai_explanations`
Caches computed SHAP and LIME local feature attributions and diagnostic narratives.
```json
{
  "_id": ObjectId("..."),
  "cache_key": "XAI-RELIANCE-2024-10-25",
  "symbol": "RELIANCE",
  "date": "2024-10-25",
  "features": [
    {"name": "rsi_14", "value": 58.4, "shap_attribution": 0.342, "lime_weight": 0.315},
    {"name": "ema_10_30_ratio", "value": 1.024, "shap_attribution": 0.281, "lime_weight": 0.260}
  ],
  "xgboost_pred": 0.68,
  "pytorch_pred": 0.65,
  "explanation_narrative": "Bullish momentum confirmed by EMA crossover and RSI support.",
  "timestamp": "2026-10-25T13:21:25.830Z"
}
```

### 8. `xai_evaluation_results`
Stores Slide 9 empirical benchmark metrics across 6 quantitative dimensions.
```json
{
  "_id": ObjectId("..."),
  "symbol": "RELIANCE",
  "shap_metrics": {
    "fidelity": 0.984,
    "stability": 0.952,
    "consistency": 0.912,
    "robustness": 0.965,
    "sparsity": 0.720,
    "latency_ms": 48.2
  },
  "lime_metrics": {
    "fidelity": 0.891,
    "stability": 0.843,
    "consistency": 0.825,
    "robustness": 0.880,
    "sparsity": 0.650,
    "latency_ms": 112.5
  },
  "timestamp": "2026-10-25T13:21:25.840Z"
}
```
