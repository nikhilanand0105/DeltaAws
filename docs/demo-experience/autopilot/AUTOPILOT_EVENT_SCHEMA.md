# QuantLens Autopilot — Telemetry & Event Schema Specification

**Standardized JSON Schemas for Operational Telemetry, REST APIs, and SSE Feeds**

---

## 1. Operational Telemetry Event Schema (`activity_feed`)

Every event streamed to the Autopilot operational activity feed conforms to the following strict JSON schema:

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "title": "AutopilotTelemetryEvent",
  "type": "object",
  "required": ["event_id", "type", "timestamp", "candle_date", "title", "detail", "status"],
  "properties": {
    "event_id": {
      "type": "string",
      "pattern": "^EVT-[0-9]{6}$",
      "description": "Unique cryptographic event identifier"
    },
    "type": {
      "type": "string",
      "enum": ["DATA", "INDICATOR", "DECISION", "RISK", "ORDER", "POSITION", "EXPLANATION", "SYSTEM"],
      "description": "Functional subsystem category"
    },
    "timestamp": {
      "type": "string",
      "pattern": "^[0-9]{2}:[0-9]{2}:[0-9]{2}\\.[0-9]{3}$",
      "description": "Wall-clock ingestion time (HH:MM:SS.mmm)"
    },
    "candle_date": {
      "type": "string",
      "format": "date",
      "description": "Simulated historical market date (YYYY-MM-DD)"
    },
    "title": {
      "type": "string",
      "description": "Human-readable concise event title"
    },
    "detail": {
      "type": "string",
      "description": "Detailed operational narrative"
    },
    "values": {
      "type": "object",
      "description": "Structured quantitative metrics associated with this event"
    },
    "status": {
      "type": "string",
      "enum": ["info", "success", "warning", "danger"],
      "description": "UI badge severity coloring"
    }
  }
}
```

### Event Type Examples

#### 1. `DECISION` (Signal Detection / Rule Evaluation)
```json
{
  "event_id": "EVT-737310",
  "type": "DECISION",
  "timestamp": "00:32:17.310",
  "candle_date": "2026-05-05",
  "title": "Bullish Golden Cross Confirmed",
  "detail": "EMA10 (₹1,456.46) crossed above EMA30 (₹1,456.40). RSI is 50.0 (safe below 65.0).",
  "values": {
    "fast_ema": 1456.46,
    "slow_ema": 1456.40,
    "rsi": 50.0,
    "action": "BUY"
  },
  "status": "success"
}
```

#### 2. `RISK` (Risk & Allocation Boundary Check)
```json
{
  "event_id": "EVT-737312",
  "type": "RISK",
  "timestamp": "00:32:17.312",
  "candle_date": "2026-05-05",
  "title": "Position Allocation Verified",
  "detail": "Allocating ₹8,741.18 (8.74% of available cash) within the 10.0% capital boundary.",
  "values": {
    "allocation_pct": 8.74,
    "max_allowed_pct": 10.0,
    "approved": true
  },
  "status": "info"
}
```

#### 3. `ORDER` (Order Execution & Fill)
```json
{
  "event_id": "EVT-741785",
  "type": "ORDER",
  "timestamp": "00:32:21.785",
  "candle_date": "2026-05-06",
  "title": "Paper SELL Filled: ORD-741780",
  "detail": "Sold 6 shares @ ₹1,430.57 | Net Result: ₹-166.41 | Reason: Stop-Loss Cutoff Hit (-1.80% <= -2.0%)",
  "values": {
    "order_id": "ORD-741780",
    "side": "SELL",
    "quantity": 6,
    "fill_price": 1430.57,
    "brokerage_fee": 4.29,
    "net_result": -166.41
  },
  "status": "danger"
}
```

---

## 2. Decision Card Schema (`current_decision_card`)

Evaluated on every single candle tick:

```json
{
  "candle_date": "2026-05-06",
  "close_price": 1431.28,
  "fast_ema": 1451.88,
  "slow_ema": 1454.77,
  "ema_crossover": "NO",
  "ema_cross_type": "NONE",
  "current_rsi": 38.45,
  "rsi_threshold": 65.0,
  "rsi_condition": "PASSED",
  "open_position_state": "ACTIVE",
  "has_position": true,
  "open_shares": 6,
  "entry_price": 1457.59,
  "stop_loss_price": 1428.44,
  "take_profit_price": 1515.89,
  "current_pnl_pct": -1.80,
  "stop_loss_hit": true,
  "take_profit_hit": false,
  "available_cash": 91250.09,
  "allocation_limit_pct": 10.0,
  "risk_validation": "APPROVED",
  "final_action": "SELL",
  "action": "SELL",
  "final_decision_title": "STOP-LOSS EXIT TRIGGERED",
  "reason": "Stop-Loss Cutoff Hit (-1.80% <= -2.0%). Protecting Virtual Capital.",
  "what_doing_now": "Stop-loss triggered (-1.80% <= -2.0%). Liquidating 6 shares of RELIANCE to protect virtual capital.",
  "narration": "Stop-loss triggered (-1.80% <= -2.0%). Liquidating 6 shares of RELIANCE to protect virtual capital.",
  "conditions": {
    "fast_above_slow": false,
    "rsi_under_threshold": true,
    "has_position": true,
    "stop_loss_hit": true,
    "take_profit_hit": false
  }
}
```

---

## 3. Trade Explanation Schema (`/explain-trade`)

```json
{
  "success": true,
  "order_id": "ORD-737315",
  "order_date": "2026-05-05",
  "order": {
    "order_id": "ORD-737315",
    "account_id": "default_paper_account",
    "symbol": "RELIANCE",
    "side": "BUY",
    "quantity": 6,
    "fill_price": 1457.59,
    "gross_value": 8745.54,
    "brokerage_fee": 4.37,
    "slippage_loss": 4.37,
    "status": "EXECUTED",
    "timestamp": "2026-05-05 00:00:00",
    "rule_reason": "Bullish Golden Cross (EMA10 1456.5 > EMA30 1456.4) with RSI 50.0 < 65.0"
  },
  "candle_metrics": {
    "close": 1456.86,
    "fast_ema": 1456.46,
    "slow_ema": 1456.40,
    "rsi": 50.0
  },
  "rule_evaluation": {
    "rule_reason": "Bullish Golden Cross (EMA10 1456.5 > EMA30 1456.4) with RSI 50.0 < 65.0",
    "strategy_name": "EMA Crossover + RSI Momentum Strategy",
    "direction": "BUY",
    "shares": 6,
    "fee_deducted": 4.37
  },
  "ml_xai_analysis": {
    "models_summary": {
      "xgboost": { "prediction": "BUY", "confidence": 0.542 },
      "pytorch_mlp": { "prediction": "BUY", "confidence": 0.589 }
    },
    "top_shap_features": [
      { "feature": "ema_30", "weight": 0.0803 },
      { "feature": "rsi_14", "weight": -0.0412 },
      { "feature": "close", "weight": 0.0385 },
      { "feature": "ema_10", "weight": 0.0271 }
    ],
    "top_lime_rules": [
      { "feature": "-0.27 < rsi_14 <= 0.49", "weight": -0.0315 },
      { "feature": "close > 1400.0", "weight": 0.0450 }
    ]
  },
  "ai_grounded_commentary": "On 2026-05-05, the 10-day EMA (1456.46) crossed above the 30-day EMA (1456.40), confirming an upward directional breakout. The RSI(14) was 50.00, safely below the 65.0 exhaustion ceiling. The risk engine verified that allocating 6 shares (₹8,745.54) satisfied the 10% maximum cash limit.",
  "storage_provenance": {
    "database": "quantlens_xai",
    "collection": "paper_orders",
    "persisted": true
  }
}
```
