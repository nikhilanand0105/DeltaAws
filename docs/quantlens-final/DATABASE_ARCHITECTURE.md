# QuantLens-XAI: Hybrid Database Architecture (SQLite + MongoDB)

## 1. Executive Summary & Design Rationale

QuantLens-XAI employs a **Hybrid Polyglot Persistence Architecture** that pairs **SQLite 3 (via SQLAlchemy 2.0 ORM)** with **MongoDB Community Edition 7.0**. This architecture optimizes for:
1. **Relational Integrity and ACID Transactions** for core system configuration, user accounts, and algorithmic trading bot states (`instance/local.db`).
2. **High-Throughput Document Persistence and Flexible Schemas** for dynamic paper trading ledgers, order book management, immutable audit trails, and multi-model Explainable AI (XAI) feature attributions (`quantlens_xai` database on `localhost:27017`).
3. **Analytical File-Based Storage** for immutable historical daily OHLCV CSVs (`data/historical/*.csv`) and pre-trained ML model binaries (`models/*.json`, `models/*.pt`).

```
+--------------------------------------------------------------------------------------------------+
|                                    QUANTLENS-XAI APPLICATION                                     |
|                               (Flask Backend + Interactive UI)                                   |
+--------------------------------------------------------------------------------------------------+
             |                                     |                                    |
             v                                     v                                    v
+-------------------------+           +-------------------------+          +-------------------------+
|     RELATIONAL STORE    |           |      DOCUMENT STORE     |          |    ANALYTICAL ASSETS    |
|   SQLite 3 / SQLAlchemy |           |   MongoDB Community 7.0 |          |    File-Based Storage   |
|   (instance/local.db)   |           |   (localhost:27017)     |          |    (data/ & models/)    |
+-------------------------+           +-------------------------+          +-------------------------+
| * accounts              |           | * paper_accounts        |          | * historical CSVs       |
| * settings              |           | * paper_positions       |          |   (RELIANCE, TCS, INFY) |
| * strategies            |           | * paper_orders          |          | * XGBoost models (.json)|
| * strategy_states       |           | * paper_trades          |          | * PyTorch MLPs (.pt)    |
| * trade_logs            |           | * paper_audit_events    |          | * Local LLM weights     |
| * local_signal_logs     |           | * paper_simulation_runs |          |   (qwen2.5:0.5b)        |
|                         |           | * xai_explanations      |          |                         |
|                         |           | * xai_evaluation_results|          |                         |
+-------------------------+           +-------------------------+          +-------------------------+
```

---

## 2. Component Responsibility Matrix

| Storage Layer | Technology | Primary Role | Data Characteristics | Consistency Model |
| :--- | :--- | :--- | :--- | :--- |
| **Relational SQL** | SQLite 3 (`instance/local.db`) | Legacy bot configuration, webhook triggers, user auth settings, bot strategies | Structured tabular, foreign-key relationships, low write volume | Strict ACID (Write-Ahead Logging) |
| **NoSQL Document** | MongoDB Community 7.0 (`quantlens_xai`) | Paper trading accounts, dynamic order ledger, trade executions, double-entry audit events, SHAP/LIME explanation caches | Hierarchical JSON/BSON, variable feature lengths, high burst write volume | Read-after-write consistency, document-level atomicity |
| **Analytical Files** | Local Filesystem (`data/`, `models/`) | Historical OHLCV market feeds, ML model weights, local LLM quantized weights | Read-only static binaries and tabular time-series | Immutable disk cache |

---

## 3. Database Split Justification

### Why Retain SQLite?
- **Zero Breaking Changes**: The existing Delta bot (`models.py`, `app.py`) operates with 6 core tables (`accounts`, `settings`, `strategies`, `strategy_states`, `trade_logs`, `local_signal_logs`). Retaining SQLite ensures 100% backward compatibility for all live broker connections, encryption salts, and legacy strategy definitions.
- **Embedded Simplicity**: SQLite requires zero network hops for local bot state transitions, executing in $<0.5\text{ ms}$.

### Why Migrate Paper Trading and XAI to MongoDB?
- **Elimination of File Lock Contention**: Prior to migration, paper trading state was stored in `data/paper_broker_state.json`. Concurrent order simulation and XAI generation led to read-write file contention.
- **Dynamic Feature Attribution Schemas**: SHAP and LIME outputs contain varying numbers of technical features (e.g., 10 features for baseline vs. 25 features for extended indicator sets). MongoDB BSON naturally accommodates variable key-value attributions without requiring schema migrations (`ALTER TABLE`).
- **Compound Indexing & Query Flexibility**: MongoDB allows compound indexes such as `(account_id, symbol)` on `paper_positions` and timestamp sorting on `paper_audit_events` for instant UI rendering.
- **Audit Immutability**: Appending audit logs into `paper_audit_events` leverages MongoDB's non-blocking capped or ordered inserts, ensuring a high-throughput, tamper-evident record.

---

## 4. Connection Pooling and Health Monitoring

The hybrid database status is monitored via the REST endpoint `/api/quantlens/db-status`, returning:
- SQLite: Connection state, database file path, integrity check (`PRAGMA integrity_check`), and table row counts.
- MongoDB: Connection state, server version, database name, and collection document counts.
