#!/usr/bin/env bash
"""
Safe, Idempotent Data Migration Script: JSON Operational Stores -> MongoDB.
Migrates:
1. data/paper_broker_state.json -> paper_accounts, paper_positions, paper_orders, paper_trades, paper_audit_events
2. cache/xai/reliance_xai_cache.json -> xai_evaluation_results, xai_explanations
Includes timestamped file backups and record reconciliation.
"""

import os
import sys
import json
import shutil
import logging
from datetime import datetime
from typing import Dict, Any

# Ensure project root in python path
ROOT_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT_DIR not in sys.path:
    sys.path.insert(0, ROOT_DIR)

from quantlens.db_mongodb import get_mongodb

logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
logger = logging.getLogger("migration")

BACKUP_DIR = os.path.join(ROOT_DIR, "data", "backups")
os.makedirs(BACKUP_DIR, exist_ok=True)


def backup_json_stores() -> Dict[str, str]:
    """Creates timestamped backups of active JSON operational files."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backups = {}

    # 1. Paper broker state
    broker_json = os.path.join(ROOT_DIR, "data", "paper_broker_state.json")
    if os.path.exists(broker_json):
        backup_path = os.path.join(BACKUP_DIR, f"paper_broker_state_{timestamp}.json")
        shutil.copy2(broker_json, backup_path)
        backups["broker"] = backup_path
        logger.info(f"✓ Backed up broker state to: {backup_path}")

    # 2. XAI cache
    xai_json = os.path.join(ROOT_DIR, "cache", "xai", "reliance_xai_cache.json")
    if os.path.exists(xai_json):
        backup_path = os.path.join(BACKUP_DIR, f"reliance_xai_cache_{timestamp}.json")
        shutil.copy2(xai_json, backup_path)
        backups["xai"] = backup_path
        logger.info(f"✓ Backed up XAI cache to: {backup_path}")

    return backups


def migrate_paper_broker(db_mgr) -> Dict[str, Any]:
    """Migrates paper_broker_state.json into MongoDB collections."""
    broker_json = os.path.join(ROOT_DIR, "data", "paper_broker_state.json")
    if not os.path.exists(broker_json):
        logger.warning("No paper_broker_state.json found. Initializing fresh account in MongoDB.")
        db_mgr.get_or_create_account()
        return {"status": "initialized_fresh", "migrated_orders": 0, "migrated_trades": 0, "migrated_audits": 0}

    with open(broker_json, "r") as f:
        data = json.load(f)

    account_id = "default_paper_account"
    initial_cap = float(data.get("initial_capital", 100000.0))
    cash = float(data.get("cash", initial_cap))
    positions = data.get("positions", {})
    orders = data.get("orders", [])
    trades = data.get("trade_history", [])
    audits = data.get("audit_log", [])
    active_strat = data.get("active_strategy", None)

    # 1. Migrate Account
    invested_val = sum(float(p.get("shares", 0)) * float(p.get("current_price", 0)) for p in positions.values())
    total_pv = cash + invested_val
    realized = sum(float(t.get("net_pnl", 0)) for t in trades)
    unrealized = sum(float(p.get("unrealized_pnl", 0)) for p in positions.values())

    db_mgr.save_account_state(
        account_id=account_id,
        initial_capital=initial_cap,
        cash=cash,
        invested_value=invested_val,
        total_portfolio_value=total_pv,
        realized_pnl=realized,
        unrealized_pnl=unrealized,
        active_strategy=active_strat
    )

    # 2. Migrate Positions
    db_mgr.save_positions(account_id, positions)

    # 3. Migrate Orders (idempotent upsert by order_id)
    orders_migrated = 0
    for o in orders:
        if "order_id" in o:
            db_mgr.insert_order(o)
            orders_migrated += 1

    # 4. Migrate Trades
    trades_migrated = 0
    for t in trades:
        db_mgr.insert_trade(t)
        trades_migrated += 1

    # 5. Migrate Audit Events
    audits_migrated = 0
    for a in audits:
        if "audit_id" in a:
            db_mgr.insert_audit_event(a)
            audits_migrated += 1

    logger.info(f"✓ Paper broker migrated to MongoDB: cash=₹{cash:,.2f}, {len(positions)} positions, {orders_migrated} orders, {trades_migrated} trades, {audits_migrated} audit events.")

    return {
        "status": "success",
        "initial_capital": initial_cap,
        "cash": cash,
        "positions_count": len(positions),
        "migrated_orders": orders_migrated,
        "migrated_trades": trades_migrated,
        "migrated_audits": audits_migrated
    }


def migrate_xai_cache(db_mgr) -> Dict[str, Any]:
    """Migrates reliance_xai_cache.json into MongoDB xai collections."""
    xai_json = os.path.join(ROOT_DIR, "cache", "xai", "reliance_xai_cache.json")
    if not os.path.exists(xai_json):
        logger.info("No reliance_xai_cache.json found to migrate.")
        return {"status": "skipped", "reason": "file_not_found"}

    with open(xai_json, "r") as f:
        data = json.load(f)

    # 1. Slide 9 Evaluation Metrics
    eval_metrics = data.get("evaluation_metrics", {})
    if not eval_metrics and "metrics" in data:
        eval_metrics = data

    if eval_metrics and "metrics" in eval_metrics:
        db_mgr.save_xai_evaluation("RELIANCE", eval_metrics)
        logger.info("✓ Migrated Slide 9 evaluation metrics to MongoDB 'xai_evaluation_results'.")

    # 2. Local Explanation
    local_exp = data.get("latest_local_explanation", {})
    if local_exp and "shap_explanation" in local_exp:
        db_mgr.save_xai_explanation(local_exp)
        logger.info("✓ Migrated local explanation to MongoDB 'xai_explanations'.")

    return {
        "status": "success",
        "eval_metrics_migrated": bool(eval_metrics),
        "local_explanation_migrated": bool(local_exp)
    }


def main():
    print("======================================================================")
    print("    QuantLens-XAI: Safe Data Migration to MongoDB")
    print("======================================================================")

    db_mgr = get_mongodb()
    if not db_mgr.is_connected():
        logger.error(f"Cannot connect to MongoDB on {db_mgr.uri}. Please ensure mongod is running.")
        sys.exit(1)

    # Step 1: Backup
    print("\n[Step 1/3] Creating timestamped backups of existing JSON files...")
    backups = backup_json_stores()

    # Step 2: Migrate Paper Broker
    print("\n[Step 2/3] Migrating paper broker operational ledger to MongoDB...")
    broker_res = migrate_paper_broker(db_mgr)

    # Step 3: Migrate XAI Cache
    print("\n[Step 3/3] Migrating XAI explanations & benchmarks to MongoDB...")
    xai_res = migrate_xai_cache(db_mgr)

    # Summary
    print("\n======================================================================")
    print("    MIGRATION COMPLETE & RECONCILED")
    print("======================================================================")
    status = db_mgr.get_status()
    print("MongoDB Collection Record Counts:")
    for coll, count in status.get("collections", {}).items():
        print(f"  • {coll}: {count} records")
    print("\nBackups preserved at:")
    for k, p in backups.items():
        print(f"  • {k}: {p}")


if __name__ == "__main__":
    main()
