# QuantLens-XAI: Paper Broker Engine & Historical Simulation Replay

**Course:** Explainable Artificial Intelligence (BCSE418L)  
**Academic Year:** 2026–27  
**Student:** Nikhil Anand  
**Reference:** Research Proposal Slide 11

---

## 1. Engine Architecture & Safety Guarantees

The **QuantLens Paper Broker** (`quantlens/paper_broker.py`) provides an original, Groww-inspired simulated Indian stock brokerage engine built from the ground up to guarantee:
1. **Strictly Virtual Funds**: Hardcoded safety banner: `PAPER TRADING — VIRTUAL FUNDS ONLY`. Zero live exchange API keys, zero real banking connections, and zero real capital risk.
2. **Double-Entry Cash Conservation**: At every tick, the ledger maintains exact balance:
   $$\text{Available Cash} + \sum_{i} (\text{Shares}_i \times \text{Current Price}_i) = \text{Total Portfolio Equity}$$
3. **Realistic Execution Modeling**:
   - Market execution slippage: $+0.05\%$ on BUY, $-0.05\%$ on SELL.
   - Brokerage & exchange turnover fee: $0.05\%$ deducted on fill.
4. **Immutable Strategy-to-Order Audit Log**: Every trade records the generating rule reason (e.g. `Simulation Rule: Golden Cross EMA10 1435.2 > EMA30 1420.5 & RSI 54.3 <= 65`) and assigns a permanent audit ID (`AUD-XXXX`).

---

## 2. Core Ledger Data Structures

### Position Record
```json
{
  "symbol": "RELIANCE",
  "shares": 7,
  "avg_price": 1276.40,
  "current_price": 1294.25,
  "unrealized_pnl": 124.95,
  "return_pct": 1.40,
  "opened_at": "2026-08-07"
}
```

### Order Record
```json
{
  "order_id": "ORD-467367",
  "timestamp": "2026-08-14",
  "symbol": "RELIANCE",
  "side": "SELL",
  "quantity": 7,
  "price": 1294.90,
  "fill_price": 1294.25,
  "gross_value": 9059.75,
  "fee": 4.53,
  "status": "EXECUTED",
  "strategy_id": "RELIANCE EMA-RSI Quantitative Strategy",
  "rule_reason": "Simulation Rule: Bearish EMA Cross"
}
```

### Audit Trail Record
```json
{
  "audit_id": "AUD-0005",
  "timestamp": "2026-08-14 10:15:00",
  "event_type": "ORDER_SELL_FILLED",
  "details": "Sold 7 shares of RELIANCE @ ₹1,294.25 | Realized PnL: ₹-115.83 (-1.21%)",
  "rule_reason": "Simulation Rule: Bearish EMA Cross",
  "cash_after": 99603.53,
  "portfolio_after": 99603.53
}
```

---

## 3. Historical Simulation Replay Engine (`quantlens/simulation_engine.py`)

The simulation engine allows researchers to take any validated strategy and replay recent historical candles (e.g., 30, 60, or 120 bars):
1. Loads the historical slice chronologically.
2. At each bar, computes EMA(10), EMA(30), and RSI(14) using data strictly up to that bar.
3. Evaluates entry/exit conditions:
   - If no position and Golden Cross triggers: Calculates $10\%$ allocation, places BUY order in the Paper Broker.
   - If position exists and Bearish Cross or Stop-Loss triggers: Closes position via SELL order.
4. Updates mark-to-market prices and records a candle-by-candle journal.
5. Saves the final state to disk (`data/paper_broker_state.json`) for seamless UI persistence across browser refreshes.
