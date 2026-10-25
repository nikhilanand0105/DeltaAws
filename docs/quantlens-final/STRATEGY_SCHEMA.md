# QuantLens-XAI: Typed Strategy Schema & Validation Rules Specification

**Course:** Explainable Artificial Intelligence (BCSE418L)  
**Academic Year:** 2026–27  
**Student:** Nikhil Anand  
**Implementation:** `quantlens/strategy_schema.py` & `quantlens/strategy_validator.py`

---

## 1. Schema Hierarchy Overview

QuantLens-XAI rejects arbitrary unvetted code execution. All natural language trading prompts are compiled into strongly-typed Pydantic v2 data models:

```
StrategyDefinition
├── IndicatorConfig
│   ├── ema_fast_period: int (2 <= v <= 200)
│   ├── ema_slow_period: int (5 <= v <= 500, must be > ema_fast_period)
│   ├── rsi_period: int (2 <= v <= 100)
│   └── rsi_threshold: float (10.0 <= v <= 90.0)
├── EntryRule
│   ├── primary_condition: str ("ema_fast crosses_above ema_slow")
│   ├── filter_condition: str ("rsi < 65")
│   ├── order_type: "market" | "limit"
│   └── direction: "BUY" | "SELL"
├── ExitRule
│   ├── reversal_condition: str ("ema_fast crosses_below ema_slow")
│   ├── stop_loss_pct: float (0.1 <= v <= 25.0)
│   └── take_profit_pct: float (0.1 <= v <= 50.0)
├── RiskManagement
│   ├── initial_capital: float (>= 1,000.0)
│   ├── max_position_allocation_pct: float (1.0 <= v <= 100.0)
│   ├── max_open_positions: int (1 <= v <= 10)
│   ├── brokerage_fee_pct: float (default 0.05%)
│   ├── slippage_pct: float (default 0.05%)
│   └── trading_mode: "paper" (strictly enforced)
└── AssumedDefault[]
    ├── field_name: str
    ├── assigned_value: Any
    ├── reason: str
    └── is_editable: bool
```

---

## 2. Pydantic v2 Class Definitions

```python
class IndicatorConfig(BaseModel):
    ema_fast_period: int = Field(default=10, ge=2, le=200)
    ema_slow_period: int = Field(default=30, ge=5, le=500)
    rsi_period: int = Field(default=14, ge=2, le=100)
    rsi_threshold: float = Field(default=65.0, ge=10.0, le=90.0)

    @field_validator("ema_slow_period")
    @classmethod
    def validate_ema_periods(cls, v, info):
        fast = info.data.get("ema_fast_period", 10)
        if v <= fast:
            raise ValueError(f"Slow EMA ({v}) must be strictly greater than Fast EMA ({fast})")
        return v
```

---

## 3. Strict Validation Rules (`validate_strategy`)

A strategy is rejected with detailed error messages if any of the following logical constraints are violated:
1. **Asset Universe Verification**: Symbol must exist within the supported liquid universe (`["RELIANCE", "TCS", "INFY", "NIFTY50"]`).
2. **Moving Average Consistency**: $\text{Fast EMA Period} < \text{Slow EMA Period}$. Contradictory periods (e.g. Fast 50, Slow 20) are caught and flagged immediately.
3. **Bounded Risk Allocation**: Max capital allocation cannot exceed $100\%$ of available equity.
4. **Positive Risk Boundaries**: $\text{Stop Loss} > 0.0\%$ and $\text{Take Profit} > 0.0\%$.
5. **Zero Real-Money Risk**: `trading_mode` cannot be set to `live` or `real`. Any attempt to set real trading mode raises an immediate validation exception.
