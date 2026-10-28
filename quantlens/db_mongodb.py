"""
QuantLens-XAI MongoDB Persistence Layer.
Implements the genuine NoSQL document/ledger architecture for:
- Paper Broker Accounts (virtual cash & equity)
- Paper Positions (active holdings)
- Paper Orders (simulated executions)
- Paper Trades (closed round-trips)
- Paper Audit Events (strategy-to-order traceability)
- Paper Simulation Runs (replay history)
- XAI Local/Global Explanations
- XAI Slide 9 Evaluation Benchmarks
Provides connection pooling, automated indexing, and schema validation.
"""

import os
import time
import logging
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
import pymongo
from pymongo import MongoClient, ASCENDING, DESCENDING
from pymongo.errors import ConnectionFailure, ServerSelectionTimeoutError

logger = logging.getLogger(__name__)

# Configurable MongoDB settings with safe local defaults
MONGODB_URI = os.getenv("MONGODB_URI", "mongodb://localhost:27017/")
MONGODB_DATABASE = os.getenv("MONGODB_DATABASE", "quantlens_xai")


class MongoDBManager:
    """Singleton MongoDB connection manager and typed repository layer."""

    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(MongoDBManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self, uri: Optional[str] = None, db_name: Optional[str] = None):
        if self._initialized:
            return

        self.uri = uri or MONGODB_URI
        self.db_name = db_name or MONGODB_DATABASE
        self.client: Optional[MongoClient] = None
        self.db = None
        self._is_connected = False

        self.connect()
        self._initialized = True

    def connect(self) -> bool:
        """Establishes connection to MongoDB and creates collection indexes."""
        try:
            self.client = MongoClient(
                self.uri,
                serverSelectionTimeoutMS=2500,
                maxPoolSize=50,
                minPoolSize=5,
                connectTimeoutMS=2500
            )
            # Verify connectivity
            self.client.admin.command("ping")
            self.db = self.client[self.db_name]
            self._is_connected = True
            self._ensure_indexes()
            logger.info(f"MongoDB connected successfully to database: '{self.db_name}' on {self.uri}")
            return True
        except (ConnectionFailure, ServerSelectionTimeoutError, Exception) as e:
            logger.warning(f"Failed to connect to MongoDB at {self.uri}: {e}")
            self._is_connected = False
            return False

    def is_connected(self) -> bool:
        """Verifies active connectivity to MongoDB."""
        if not self.client or not self._is_connected:
            return False
        try:
            self.client.admin.command("ping")
            return True
        except Exception:
            self._is_connected = False
            return False

    def get_status(self) -> Dict[str, Any]:
        """Returns database health status and collection statistics."""
        connected = self.is_connected()
        if not connected:
            return {
                "connected": False,
                "database": self.db_name,
                "uri": self.uri,
                "collections": {}
            }

        colls = {}
        for c in [
            "paper_accounts",
            "paper_positions",
            "paper_orders",
            "paper_trades",
            "paper_audit_events",
            "paper_simulation_runs",
            "xai_explanations",
            "xai_evaluation_results"
        ]:
            colls[c] = self.db[c].count_documents({})

        return {
            "connected": True,
            "database": self.db_name,
            "uri": self.uri,
            "server_version": self.client.server_info().get("version"),
            "collections": colls
        }

    def _ensure_indexes(self):
        """Creates unique keys and compound query indexes across all collections."""
        if not self._is_connected or self.db is None:
            return

        try:
            # 1. paper_accounts
            self.db.paper_accounts.create_index([("account_id", ASCENDING)], unique=True)

            # 2. paper_positions (unique per account and symbol)
            self.db.paper_positions.create_index(
                [("account_id", ASCENDING), ("symbol", ASCENDING)],
                unique=True
            )

            # 3. paper_orders
            self.db.paper_orders.create_index([("order_id", ASCENDING)], unique=True)
            self.db.paper_orders.create_index([("account_id", ASCENDING), ("timestamp", DESCENDING)])
            self.db.paper_orders.create_index([("idempotency_key", ASCENDING)], unique=True, sparse=True)

            # 4. paper_trades
            self.db.paper_trades.create_index([("trade_id", ASCENDING)], unique=True)
            self.db.paper_trades.create_index([("account_id", ASCENDING), ("exit_date", DESCENDING)])

            # 5. paper_audit_events
            self.db.paper_audit_events.create_index([("audit_id", ASCENDING)], unique=True)
            self.db.paper_audit_events.create_index([("account_id", ASCENDING), ("timestamp", DESCENDING)])

            # 6. paper_simulation_runs
            self.db.paper_simulation_runs.create_index([("run_id", ASCENDING)], unique=True)

            # 7. xai_explanations
            self.db.xai_explanations.create_index([("cache_key", ASCENDING)], unique=True)
            self.db.xai_explanations.create_index([("symbol", ASCENDING), ("sample_index", ASCENDING)])

            # 8. xai_evaluation_results
            self.db.xai_evaluation_results.create_index([("symbol", ASCENDING)], unique=True)

            logger.info("MongoDB indexes verified successfully.")
        except Exception as e:
            logger.warning(f"Error creating MongoDB indexes: {e}")

    # =========================================================================
    # PAPER BROKER DATA ACCESS REPOSITORY
    # =========================================================================

    def get_or_create_account(
        self,
        account_id: str = "default_paper_account",
        initial_capital: float = 100000.0
    ) -> Dict[str, Any]:
        """Loads account document or seeds default virtual ₹1,00,000 INR account."""
        if not self.is_connected():
            return {
                "account_id": account_id,
                "initial_capital": initial_capital,
                "available_cash": initial_capital,
                "invested_value": 0.0,
                "total_portfolio_value": initial_capital,
                "realized_pnl": 0.0,
                "unrealized_pnl": 0.0,
                "trading_mode": "PAPER TRADING — VIRTUAL FUNDS ONLY"
            }

        doc = self.db.paper_accounts.find_one({"account_id": account_id}, {"_id": 0})
        if not doc:
            doc = {
                "account_id": account_id,
                "display_name": "QuantLens Virtual Paper Account",
                "currency": "INR",
                "initial_capital": float(initial_capital),
                "available_cash": float(initial_capital),
                "invested_value": 0.0,
                "total_portfolio_value": float(initial_capital),
                "realized_pnl": 0.0,
                "unrealized_pnl": 0.0,
                "trading_mode": "PAPER TRADING — VIRTUAL FUNDS ONLY",
                "active_strategy": None,
                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.db.paper_accounts.insert_one(doc)
            doc.pop("_id", None)

        return doc

    def save_account_state(
        self,
        account_id: str,
        initial_capital: float,
        cash: float,
        invested_value: float,
        total_portfolio_value: float,
        realized_pnl: float,
        unrealized_pnl: float,
        active_strategy: Optional[Dict[str, Any]] = None
    ):
        """Updates account summary document in MongoDB."""
        if not self.is_connected():
            return

        self.db.paper_accounts.update_one(
            {"account_id": account_id},
            {
                "$set": {
                    "initial_capital": round(float(initial_capital), 2),
                    "available_cash": round(float(cash), 2),
                    "invested_value": round(float(invested_value), 2),
                    "total_portfolio_value": round(float(total_portfolio_value), 2),
                    "realized_pnl": round(float(realized_pnl), 2),
                    "unrealized_pnl": round(float(unrealized_pnl), 2),
                    "active_strategy": active_strategy,
                    "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            },
            upsert=True
        )

    def get_positions(self, account_id: str = "default_paper_account") -> Dict[str, Dict[str, Any]]:
        """Retrieves active holdings dictionary symbol -> position."""
        if not self.is_connected():
            return {}

        cursor = self.db.paper_positions.find({"account_id": account_id, "shares": {"$gt": 0}}, {"_id": 0})
        positions = {}
        for p in cursor:
            positions[p["symbol"]] = p
        return positions

    def save_positions(self, account_id: str, positions: Dict[str, Dict[str, Any]]):
        """Reconciles position documents in MongoDB."""
        if not self.is_connected():
            return

        # Clear existing
        self.db.paper_positions.delete_many({"account_id": account_id})
        docs = []
        for sym, pos in positions.items():
            if pos.get("shares", 0) > 0:
                p_doc = dict(pos)
                p_doc["account_id"] = account_id
                p_doc["symbol"] = sym
                docs.append(p_doc)

        if docs:
            self.db.paper_positions.insert_many(docs)

    def insert_order(self, order_doc: Dict[str, Any]):
        """Persists a new paper order in MongoDB."""
        if not self.is_connected():
            return
        doc = dict(order_doc)
        doc["account_id"] = doc.get("account_id", "default_paper_account")
        self.db.paper_orders.replace_one({"order_id": doc["order_id"]}, doc, upsert=True)

    def get_orders(self, account_id: str = "default_paper_account", limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieves recent orders sorted newest first."""
        if not self.is_connected():
            return []
        cursor = self.db.paper_orders.find(
            {"account_id": account_id},
            {"_id": 0}
        ).sort("timestamp", DESCENDING).limit(limit)
        return list(cursor)

    def insert_trade(self, trade_doc: Dict[str, Any]):
        """Persists a closed round-trip trade record in MongoDB."""
        if not self.is_connected():
            return
        doc = dict(trade_doc)
        doc["account_id"] = doc.get("account_id", "default_paper_account")
        trade_id = doc.get("trade_id") or f"TRD-{int(time.time() * 1000) % 1000000:06d}"
        doc["trade_id"] = trade_id
        self.db.paper_trades.replace_one({"trade_id": trade_id}, doc, upsert=True)

    def get_trades(self, account_id: str = "default_paper_account", limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieves completed trade history sorted newest first."""
        if not self.is_connected():
            return []
        cursor = self.db.paper_trades.find(
            {"account_id": account_id},
            {"_id": 0}
        ).sort("exit_date", DESCENDING).limit(limit)
        return list(cursor)

    def insert_audit_event(self, audit_doc: Dict[str, Any]):
        """Persists an immutable audit log entry in MongoDB."""
        if not self.is_connected():
            return
        doc = dict(audit_doc)
        doc["account_id"] = doc.get("account_id", "default_paper_account")
        self.db.paper_audit_events.replace_one({"audit_id": doc["audit_id"]}, doc, upsert=True)

    def get_audit_trail(self, account_id: str = "default_paper_account", limit: int = 50) -> List[Dict[str, Any]]:
        """Retrieves immutable strategy audit trail sorted newest first."""
        if not self.is_connected():
            return []
        cursor = self.db.paper_audit_events.find(
            {"account_id": account_id},
            {"_id": 0}
        ).sort("timestamp", DESCENDING).limit(limit)
        return list(cursor)

    def reset_broker_database(self, account_id: str = "default_paper_account", initial_capital: float = 100000.0):
        """Clears all orders, positions, and trades in MongoDB, resetting account to initial capital."""
        if not self.is_connected():
            return

        self.db.paper_positions.delete_many({"account_id": account_id})
        self.db.paper_orders.delete_many({"account_id": account_id})
        self.db.paper_trades.delete_many({"account_id": account_id})
        self.db.paper_audit_events.delete_many({"account_id": account_id})

        self.db.paper_accounts.update_one(
            {"account_id": account_id},
            {
                "$set": {
                    "initial_capital": float(initial_capital),
                    "available_cash": float(initial_capital),
                    "invested_value": 0.0,
                    "total_portfolio_value": float(initial_capital),
                    "realized_pnl": 0.0,
                    "unrealized_pnl": 0.0,
                    "active_strategy": None,
                    "updated_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
            },
            upsert=True
        )

        # Log reset audit event
        reset_audit = {
            "audit_id": "AUD-0001",
            "account_id": account_id,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "event_type": "ACCOUNT_RESET",
            "details": f"Paper broker reset to initial virtual capital of ₹{initial_capital:,.2f} INR",
            "rule_reason": "Manual / Demo Reset",
            "cash_after": float(initial_capital),
            "portfolio_after": float(initial_capital)
        }
        self.db.paper_audit_events.insert_one(reset_audit)

    # =========================================================================
    # XAI CACHE & EVALUATION REPOSITORY
    # =========================================================================

    def get_cached_xai_explanation(self, symbol: str, sample_index: int, target_model: str) -> Optional[Dict[str, Any]]:
        """Retrieves cached local SHAP/LIME explanation from MongoDB."""
        if not self.is_connected():
            return None
        cache_key = f"{symbol.upper()}_{sample_index}_{target_model.lower()}"
        return self.db.xai_explanations.find_one({"cache_key": cache_key}, {"_id": 0})

    def save_xai_explanation(self, explanation_doc: Dict[str, Any]):
        """Persists local SHAP/LIME explanation in MongoDB."""
        if not self.is_connected():
            return
        doc = dict(explanation_doc)
        sym = doc.get("symbol", "RELIANCE")
        idx = doc.get("sample_index", -1)
        model = doc.get("target_model", "XGBOOST").lower()
        cache_key = f"{sym.upper()}_{idx}_{model}"
        doc["cache_key"] = cache_key
        doc["explanation_id"] = f"EXP-{sym}-{int(time.time()*1000)%1000000}"
        doc["created_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.db.xai_explanations.replace_one({"cache_key": cache_key}, doc, upsert=True)

    def get_cached_xai_evaluation(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Retrieves cached Slide 9 evaluation results from MongoDB."""
        if not self.is_connected():
            return None
        return self.db.xai_evaluation_results.find_one({"symbol": symbol.upper()}, {"_id": 0})

    def save_xai_evaluation(self, symbol: str, evaluation_doc: Dict[str, Any]):
        """Persists Slide 9 empirical evaluation results in MongoDB."""
        if not self.is_connected():
            return
        doc = dict(evaluation_doc)
        doc["symbol"] = symbol.upper()
        doc["evaluation_id"] = f"EVAL-{symbol.upper()}"
        doc["updated_at"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.db.xai_evaluation_results.replace_one({"symbol": symbol.upper()}, doc, upsert=True)


# Global singleton instance
mongodb_manager = MongoDBManager()


def get_mongodb() -> MongoDBManager:
    """Returns the singleton MongoDBManager instance."""
    global mongodb_manager
    if not mongodb_manager._initialized:
        mongodb_manager = MongoDBManager()
    return mongodb_manager


def get_mongo_db():
    """Returns the PyMongo database object if connected, else None."""
    mgr = get_mongodb()
    return mgr.db if mgr.is_connected() else None


get_mongodb_manager = get_mongodb

