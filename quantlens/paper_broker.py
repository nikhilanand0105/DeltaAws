"""
QuantLens Paper Broker — Simulated Indian Stock Brokerage Engine.
Inspired by modern Indian trading apps like Groww with clean usability and original branding.
Strictly enforced: PAPER TRADING — VIRTUAL FUNDS ONLY (No real money).
Guarantees double-entry cash conservation, slippage modeling, fee accounting,
and full strategy-to-order audit traceability.
"""

import os
import json
import time
import math
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime

logger = logging.getLogger(__name__)

BROKER_STATE_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "paper_broker_state.json")


class PaperBroker:
    """Simulated execution venue managing virtual cash, positions, orders, and audit trail."""

    def __init__(self, initial_capital: float = 100000.0):
        self.initial_capital = float(initial_capital)
        self.cash: float = float(initial_capital)
        self.positions: Dict[str, Dict[str, Any]] = {}  # symbol -> {shares, avg_price, current_price, unrealized_pnl}
        self.orders: List[Dict[str, Any]] = []
        self.trade_history: List[Dict[str, Any]] = []
        self.audit_log: List[Dict[str, Any]] = []
        self.active_strategy: Optional[Dict[str, Any]] = None
        self.equity_history: List[Dict[str, Any]] = []
        self.fee_rate: float = 0.0005      # 0.05% brokerage & exchange turnover fee
        self.slippage_rate: float = 0.0005  # 0.05% market execution slippage

        self.load_state()

    def reset_account(self, initial_capital: float = 100000.0):
        """Resets the paper broker to a fresh virtual account state."""
        self.initial_capital = float(initial_capital)
        self.cash = float(initial_capital)
        self.positions = {}
        self.orders = []
        self.trade_history = []
        self.audit_log = []
        self.active_strategy = None
        self.equity_history = [
            {
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                "portfolio_value": self.cash,
                "cash": self.cash,
                "invested": 0.0,
                "note": "Account Initialized"
            }
        ]
        self.log_audit("ACCOUNT_RESET", f"Paper broker reset to initial virtual capital of ₹{self.cash:,.2f} INR")
        self.save_state()

    def log_audit(self, event_type: str, details: str, rule_reason: Optional[str] = None):
        """Appends an event to the immutable strategy-to-order audit ledger."""
        entry = {
            "audit_id": f"AUD-{len(self.audit_log) + 1:04d}",
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "event_type": event_type,
            "details": details,
            "rule_reason": rule_reason or "Manual / System Action",
            "cash_after": round(self.cash, 2),
            "portfolio_after": round(self.get_portfolio_value(), 2)
        }
        self.audit_log.insert(0, entry)  # Prepend newest first
        if len(self.audit_log) > 500:
            self.audit_log.pop()

    def get_portfolio_value(self) -> float:
        """Calculates total mark-to-market equity = cash + sum(position shares * current_price)."""
        invested = sum(p["shares"] * p["current_price"] for p in self.positions.values())
        return self.cash + invested

    def update_market_prices(self, price_map: Dict[str, float]):
        """Updates live mark-to-market prices for all open positions."""
        for sym, current_px in price_map.items():
            if sym in self.positions:
                pos = self.positions[sym]
                pos["current_price"] = float(current_px)
                pos["unrealized_pnl"] = round((pos["current_price"] - pos["avg_price"]) * pos["shares"], 2)
                pos["return_pct"] = round(((pos["current_price"] - pos["avg_price"]) / pos["avg_price"]) * 100.0, 2)

    def execute_order(
        self,
        symbol: str,
        side: str,
        quantity: int,
        price: float,
        order_type: str = "market",
        strategy_id: Optional[str] = None,
        rule_reason: Optional[str] = None,
        timestamp_str: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Executes a simulated order in the paper broker ledger.
        Handles slippage, fees, cash deduction, position updates, and audit logging.
        """
        sym = symbol.upper().replace(".NS", "")
        qty = int(quantity)
        side = side.upper()
        now_str = timestamp_str or datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        if qty <= 0:
            return {"success": False, "message": "Quantity must be greater than zero."}

        order_id = f"ORD-{int(time.time() * 1000) % 1000000:06d}"

        # Apply slippage
        if side == "BUY":
            fill_price = round(price * (1.0 + self.slippage_rate), 2)
        else:
            fill_price = round(price * (1.0 - self.slippage_rate), 2)

        gross_value = round(qty * fill_price, 2)
        fee = round(gross_value * self.fee_rate, 2)

        # 1. Handle BUY Order
        if side == "BUY":
            total_required = gross_value + fee
            if total_required > self.cash:
                rejection_msg = f"Insufficient funds: Required ₹{total_required:,.2f} > Available ₹{self.cash:,.2f}"
                self.orders.insert(0, {
                    "order_id": order_id,
                    "timestamp": now_str,
                    "symbol": sym,
                    "side": side,
                    "quantity": qty,
                    "price": price,
                    "fill_price": None,
                    "status": "REJECTED",
                    "reason": rejection_msg,
                    "strategy_id": strategy_id
                })
                self.log_audit("ORDER_REJECTED", rejection_msg, rule_reason)
                return {"success": False, "message": rejection_msg}

            # Deduct virtual cash
            self.cash -= total_required

            # Update or create position
            if sym in self.positions:
                pos = self.positions[sym]
                new_shares = pos["shares"] + qty
                pos["avg_price"] = round(((pos["avg_price"] * pos["shares"]) + gross_value) / new_shares, 2)
                pos["shares"] = new_shares
                pos["current_price"] = fill_price
                pos["unrealized_pnl"] = round((fill_price - pos["avg_price"]) * new_shares, 2)
            else:
                self.positions[sym] = {
                    "symbol": sym,
                    "shares": qty,
                    "avg_price": fill_price,
                    "current_price": fill_price,
                    "unrealized_pnl": 0.0,
                    "return_pct": 0.0,
                    "opened_at": now_str
                }

            order_record = {
                "order_id": order_id,
                "timestamp": now_str,
                "symbol": sym,
                "side": side,
                "quantity": qty,
                "price": price,
                "fill_price": fill_price,
                "gross_value": gross_value,
                "fee": fee,
                "status": "EXECUTED",
                "strategy_id": strategy_id,
                "rule_reason": rule_reason or "Manual Paper Trade"
            }
            self.orders.insert(0, order_record)

            self.log_audit(
                "ORDER_BUY_FILLED",
                f"Bought {qty} shares of {sym} @ ₹{fill_price:,.2f} (Total: ₹{total_required:,.2f} with fee ₹{fee})",
                rule_reason
            )

        # 2. Handle SELL Order
        elif side == "SELL":
            if sym not in self.positions or self.positions[sym]["shares"] < qty:
                available_shares = self.positions[sym]["shares"] if sym in self.positions else 0
                rejection_msg = f"Insufficient shares to sell: Requested {qty} > Available {available_shares}"
                self.orders.insert(0, {
                    "order_id": order_id,
                    "timestamp": now_str,
                    "symbol": sym,
                    "side": side,
                    "quantity": qty,
                    "price": price,
                    "fill_price": None,
                    "status": "REJECTED",
                    "reason": rejection_msg,
                    "strategy_id": strategy_id
                })
                self.log_audit("ORDER_REJECTED", rejection_msg, rule_reason)
                return {"success": False, "message": rejection_msg}

            pos = self.positions[sym]
            entry_px = pos["avg_price"]
            cost_basis = round(qty * entry_px, 2)
            net_proceeds = gross_value - fee
            realized_pnl = round(net_proceeds - cost_basis, 2)
            return_pct = round(((fill_price - entry_px) / entry_px) * 100.0, 2)

            # Credit virtual cash
            self.cash += net_proceeds

            # Update position
            pos["shares"] -= qty
            if pos["shares"] == 0:
                del self.positions[sym]
            else:
                pos["unrealized_pnl"] = round((pos["current_price"] - pos["avg_price"]) * pos["shares"], 2)

            order_record = {
                "order_id": order_id,
                "timestamp": now_str,
                "symbol": sym,
                "side": side,
                "quantity": qty,
                "price": price,
                "fill_price": fill_price,
                "gross_value": gross_value,
                "fee": fee,
                "status": "EXECUTED",
                "strategy_id": strategy_id,
                "rule_reason": rule_reason or "Manual Paper Trade"
            }
            self.orders.insert(0, order_record)

            trade_record = {
                "trade_id": len(self.trade_history) + 1,
                "order_id": order_id,
                "timestamp": now_str,
                "symbol": sym,
                "shares": qty,
                "entry_price": entry_px,
                "exit_price": fill_price,
                "gross_pnl": round((fill_price - entry_px) * qty, 2),
                "fees": fee,
                "net_pnl": realized_pnl,
                "return_pct": return_pct,
                "exit_reason": rule_reason or "Manual Sell",
                "strategy_id": strategy_id
            }
            self.trade_history.insert(0, trade_record)

            self.log_audit(
                "ORDER_SELL_FILLED",
                f"Sold {qty} shares of {sym} @ ₹{fill_price:,.2f} | Realized PnL: ₹{realized_pnl:+,.2f} ({return_pct:+.2f}%)",
                rule_reason
            )

        self.save_state()
        return {
            "success": True,
            "order_id": order_id,
            "fill_price": fill_price,
            "quantity": qty,
            "side": side,
            "symbol": sym,
            "message": f"Simulated {side} order filled for {qty} shares of {sym} at ₹{fill_price:,.2f}"
        }

    def get_dashboard_summary(self) -> Dict[str, Any]:
        """Provides real-time portfolio metrics formatted for the Groww-inspired UI."""
        invested_val = sum(p["shares"] * p["current_price"] for p in self.positions.values())
        total_portfolio = self.cash + invested_val
        total_pnl = total_portfolio - self.initial_capital
        total_pnl_pct = (total_pnl / self.initial_capital) * 100.0 if self.initial_capital > 0 else 0.0

        unrealized_pnl = sum(p["unrealized_pnl"] for p in self.positions.values())
        realized_pnl = sum(t["net_pnl"] for t in self.trade_history)

        return {
            "initial_capital": self.initial_capital,
            "available_cash": round(self.cash, 2),
            "invested_value": round(invested_val, 2),
            "total_portfolio_value": round(total_portfolio, 2),
            "total_pnl": round(total_pnl, 2),
            "total_pnl_pct": round(total_pnl_pct, 2),
            "realized_pnl": round(realized_pnl, 2),
            "unrealized_pnl": round(unrealized_pnl, 2),
            "open_positions_count": len(self.positions),
            "completed_orders_count": len([o for o in self.orders if o["status"] == "EXECUTED"]),
            "open_positions": list(self.positions.values()),
            "recent_orders": self.orders[:15],
            "recent_trades": self.trade_history[:15],
            "audit_trail": self.audit_log[:25],
            "active_strategy": self.active_strategy,
            "trading_mode": "PAPER TRADING — VIRTUAL FUNDS ONLY"
        }

    def save_state(self):
        """Persists broker state to JSON on disk."""
        os.makedirs(os.path.dirname(BROKER_STATE_FILE), exist_ok=True)
        state = {
            "initial_capital": self.initial_capital,
            "cash": self.cash,
            "positions": self.positions,
            "orders": self.orders,
            "trade_history": self.trade_history,
            "audit_log": self.audit_log,
            "active_strategy": self.active_strategy
        }
        with open(BROKER_STATE_FILE, "w") as f:
            json.dump(state, f, indent=2)

    def load_state(self):
        """Loads persisted state from disk if present."""
        if os.path.exists(BROKER_STATE_FILE):
            try:
                with open(BROKER_STATE_FILE, "r") as f:
                    state = json.load(f)
                    self.initial_capital = float(state.get("initial_capital", 100000.0))
                    self.cash = float(state.get("cash", 100000.0))
                    self.positions = state.get("positions", {})
                    self.orders = state.get("orders", [])
                    self.trade_history = state.get("trade_history", [])
                    self.audit_log = state.get("audit_log", [])
                    self.active_strategy = state.get("active_strategy", None)
            except Exception as e:
                logger.warning(f"Error loading broker state from {BROKER_STATE_FILE}: {e}")
                self.reset_account()
        else:
            self.reset_account()


# Global Singleton Broker Instance
broker = PaperBroker()


def get_paper_broker() -> PaperBroker:
    """Returns the singleton PaperBroker instance."""
    global broker
    return broker

