# QuantLens-XAI: Relational Database Schema (SQLite 3 / SQLAlchemy)

## 1. Overview
The relational storage layer is managed by **SQLAlchemy 2.0** on top of **SQLite 3** (`instance/local.db`). It contains 6 tables responsible for system configuration, broker credentials, trading bot operational states, and signal history.

---

## 2. Table Definitions & Entity Relationships

```
+-------------------+        1:N       +-------------------+
|     accounts      | ---------------- |  strategy_states  |
+-------------------+                  +-------------------+
| id (PK)           |                  | id (PK)           |
| broker_name       |                  | account_id (FK)   |
| api_key           |                  | strategy_id (FK)  |
| is_active         |                  | state             |
+-------------------+                  +-------------------+
          | 1:N
          v
+-------------------+                  +-------------------+
|    trade_logs     |                  |    strategies     |
+-------------------+                  +-------------------+
| id (PK)           |                  | id (PK)           |
| account_id (FK)   |                  | name              |
| symbol            |                  | script / json     |
| pnl               |                  | is_active         |
+-------------------+                  +-------------------+
```

---

## 3. Comprehensive Table Schemas

### 1. `accounts`
Stores multi-broker integration configurations (e.g., Zerodha, Angel One, Paper Trading).
- `id` (INTEGER, Primary Key, Autoincrement)
- `broker_name` (VARCHAR(50), Not Null)
- `api_key` (VARCHAR(255), Nullable, Encrypted at rest)
- `api_secret` (VARCHAR(255), Nullable, Encrypted at rest)
- `user_id` (VARCHAR(100), Nullable)
- `is_active` (BOOLEAN, Default: True)
- `created_at` (DATETIME, Default: CURRENT_TIMESTAMP)

### 2. `settings`
Global application settings and operational flags.
- `id` (INTEGER, Primary Key, Autoincrement)
- `key` (VARCHAR(100), Unique, Not Null)
- `value` (TEXT, Not Null)
- `updated_at` (DATETIME, Default: CURRENT_TIMESTAMP)

### 3. `strategies`
Configured trading strategies defined via JSON configuration or legacy script rules.
- `id` (INTEGER, Primary Key, Autoincrement)
- `name` (VARCHAR(100), Unique, Not Null)
- `description` (TEXT, Nullable)
- `strategy_type` (VARCHAR(50), Default: 'technical')
- `parameters_json` (TEXT, Nullable)
- `is_active` (BOOLEAN, Default: True)
- `created_at` (DATETIME, Default: CURRENT_TIMESTAMP)

### 4. `strategy_states`
Runtime execution states of bot strategies linked to specific broker accounts.
- `id` (INTEGER, Primary Key, Autoincrement)
- `strategy_id` (INTEGER, Foreign Key -> strategies.id)
- `account_id` (INTEGER, Foreign Key -> accounts.id)
- `state` (VARCHAR(50), Default: 'IDLE')
- `last_signal` (VARCHAR(50), Nullable)
- `last_signal_time` (DATETIME, Nullable)
- `position_size` (INTEGER, Default: 0)
- `unrealized_pnl` (FLOAT, Default: 0.0)

### 5. `trade_logs`
Historical trade execution ledger for the automated bot runtime.
- `id` (INTEGER, Primary Key, Autoincrement)
- `account_id` (INTEGER, Foreign Key -> accounts.id)
- `symbol` (VARCHAR(20), Not Null)
- `action` (VARCHAR(10), Not Null) - `BUY` or `SELL`
- `quantity` (INTEGER, Not Null)
- `price` (FLOAT, Not Null)
- `pnl` (FLOAT, Default: 0.0)
- `timestamp` (DATETIME, Default: CURRENT_TIMESTAMP)

### 6. `local_signal_logs`
Raw signal audit capturing webhook payloads and technical indicators prior to execution.
- `id` (INTEGER, Primary Key, Autoincrement)
- `symbol` (VARCHAR(20), Not Null)
- `signal` (VARCHAR(20), Not Null)
- `indicator_snapshot` (TEXT, Nullable)
- `processed` (BOOLEAN, Default: True)
- `timestamp` (DATETIME, Default: CURRENT_TIMESTAMP)

---

## 4. Integrity and Verification
Database integrity is verified at boot time using:
```sql
PRAGMA integrity_check;
```
All tables utilize foreign key constraints and transactional rollback on execution exceptions.
