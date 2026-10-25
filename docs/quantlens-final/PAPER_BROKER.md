# QuantLens-XAI: Paper Broker & Order Execution Engine

## 1. Overview
The Groww-inspired Paper Broker simulates an institutional execution broker with realistic order management, portfolio valuation, fee structures, and strict double-entry accounting.

---

## 2. Architecture & MongoDB Persistence
The paper broker persists all transactional state directly into **MongoDB Community 7.0**:
- `paper_accounts`: Virtual capital ($₹10,00,000$ base), available cash, and realized P&L.
- `paper_positions`: Live stock holdings with average purchase price and unrealized P&L.
- `paper_orders`: Complete orders ledger with unique IDs (`ORD-YYYYMMDD-XXXX`) and idempotency keys.
- `paper_trades`: Closed round-trip trades with realized gain/loss and holding duration.
- `paper_audit_events`: Tamper-evident double-entry audit trail (`AUD-YYYYMMDD-XXXX`).

---

## 3. Double-Entry Accounting Invariant
To ensure mathematical conservation of capital:
$$\Delta \text{Cash} + \Delta \text{HoldingsValue} + \text{BrokerageFees} + \text{RealizedLoss} = 0$$
Every trade execution simultaneously credits/debits cash and positions, recording an immutable audit event in `paper_audit_events`.
