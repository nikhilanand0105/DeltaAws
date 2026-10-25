"""
QuantLens Simulation Engine — Historical Replay & Automated Strategy Simulation.
Enables step-by-step or windowed replay of historical candles against the QuantLens Paper Broker.
Simulates real market order generation with slippage, fees, and strategy audit trail.
"""

import os
import logging
from typing import Dict, Any, List, Optional
import pandas as pd
import numpy as np

from quantlens.data_loader import load_historical_ohlcv
from quantlens.feature_engineering import extract_technical_features, FEATURE_COLUMNS
from quantlens.strategy_schema import StrategyDefinition
from quantlens.paper_broker import PaperBroker, get_paper_broker

logger = logging.getLogger(__name__)


class SimulationEngine:
    """Historical market simulator that drives the PaperBroker using real historical data."""

    def __init__(self, broker: Optional[PaperBroker] = None):
        self.broker = broker or get_paper_broker()

    def run_replay(
        self,
        strategy: StrategyDefinition,
        window_bars: int = 120,
        reset_broker_first: bool = False,
        ml_filter: bool = False
    ) -> Dict[str, Any]:
        """
        Replays the last `window_bars` historical daily bars for the strategy symbol.
        Simulates order execution in the PaperBroker according to the strategy rules.
        """
        symbol = strategy.symbol
        if reset_broker_first:
            self.broker.reset_account(strategy.risk_config.initial_capital)

        # 1. Load historical data
        raw_df = load_historical_ohlcv(symbol)
        featured_df = extract_technical_features(raw_df)

        if len(featured_df) < window_bars:
            window_bars = len(featured_df)

        # Focus on the replay slice (e.g. most recent window_bars)
        replay_df = featured_df.iloc[-window_bars:].copy()

        # Strategy parameters
        fast_period = strategy.indicators.ema_fast_period
        slow_period = strategy.indicators.ema_slow_period
        rsi_period = strategy.indicators.rsi_period
        rsi_threshold = strategy.indicators.rsi_threshold
        fast_col = f"ema_{fast_period}"
        slow_col = f"ema_{slow_period}"
        rsi_col = f"rsi_{rsi_period}"

        # Ensure columns exist
        if fast_col not in replay_df.columns:
            replay_df[fast_col] = replay_df["close"].ewm(span=fast_period, adjust=False).mean()
        if slow_col not in replay_df.columns:
            replay_df[slow_col] = replay_df["close"].ewm(span=slow_period, adjust=False).mean()
        if rsi_col not in replay_df.columns:
            delta = replay_df["close"].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=rsi_period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=rsi_period).mean()
            rs = gain / loss.replace(0, np.nan)
            replay_df[rsi_col] = 100 - (100 / (1 + rs)).fillna(50)

        max_alloc_pct = strategy.risk_config.max_position_allocation_pct / 100.0
        stop_loss_pct = strategy.exit_rule.stop_loss_pct / 100.0
        take_profit_pct = strategy.exit_rule.take_profit_pct / 100.0
        max_positions = strategy.risk_config.max_open_positions

        replay_journal = []
        orders_triggered = 0

        # Optional ML model evaluator
        ml_models = None
        if ml_filter:
            try:
                from quantlens.ml_models import MLModelManager
                ml_models = MLModelManager()
                ml_models.load_saved_models(symbol)
            except Exception as e:
                logger.warning(f"ML models could not be loaded for simulation: {e}")
                ml_models = None

        sym_key = symbol.replace(".NS", "")

        for i in range(1, len(replay_df)):
            prev_row = replay_df.iloc[i - 1]
            curr_row = replay_df.iloc[i]

            date_val = curr_row["date"]
            if hasattr(date_val, "strftime"):
                date_str = date_val.strftime("%Y-%m-%d")
            else:
                date_str = str(date_val)[:10]

            close_price = float(curr_row["close"])
            fast_ema = float(curr_row[fast_col])
            slow_ema = float(curr_row[slow_col])
            rsi_val = float(curr_row[rsi_col]) if not np.isnan(curr_row[rsi_col]) else 50.0

            prev_fast = float(prev_row[fast_col])
            prev_slow = float(prev_row[slow_col])

            # Update broker mark-to-market prices
            self.broker.update_market_prices({sym_key: close_price})

            # Check positions
            has_position = sym_key in self.broker.positions and self.broker.positions[sym_key]["shares"] > 0
            pos_count = len([p for p in self.broker.positions.values() if p["shares"] > 0])

            signal = "HOLD"
            reason = "No crossover or threshold triggered"
            order_res = None

            # ML prediction for current bar if available
            ml_pred = None
            if ml_models:
                try:
                    # Single row feature vector
                    feat_cols = ml_models.feature_names
                    if all(c in curr_row for c in feat_cols):
                        X_bar = curr_row[feat_cols].values.reshape(1, -1)
                        preds = ml_models.predict(X_bar)
                        ml_pred = {
                            "xgboost": preds["xgboost_label"][0],
                            "pytorch": preds["pytorch_label"][0],
                            "consensus": preds["consensus_label"][0]
                        }
                except Exception:
                    pass

            # 1. EVALUATE EXIT CONDITIONS
            if has_position:
                pos = self.broker.positions[sym_key]
                pnl_pct = (close_price - pos["avg_price"]) / pos["avg_price"]

                exit_triggered = False
                exit_rule = ""

                if pnl_pct <= -stop_loss_pct:
                    exit_triggered = True
                    exit_rule = f"Stop Loss Hit ({pnl_pct * 100:.2f}% <= -{stop_loss_pct * 100:.1f}%)"
                elif pnl_pct >= take_profit_pct:
                    exit_triggered = True
                    exit_rule = f"Take Profit Target Hit ({pnl_pct * 100:.2f}% >= +{take_profit_pct * 100:.1f}%)"
                elif prev_fast >= prev_slow and fast_ema < slow_ema:
                    exit_triggered = True
                    exit_rule = f"Bearish EMA Cross (EMA{fast_period} {fast_ema:.1f} < EMA{slow_period} {slow_ema:.1f})"

                if exit_triggered:
                    signal = "SELL"
                    reason = exit_rule
                    order_res = self.broker.execute_order(
                        symbol=sym_key,
                        side="SELL",
                        quantity=pos["shares"],
                        price=close_price,
                        order_type="market",
                        strategy_id=strategy.strategy_name,
                        rule_reason=f"Simulation Rule: {exit_rule}",
                        timestamp_str=date_str
                    )
                    orders_triggered += 1

            # 2. EVALUATE ENTRY CONDITIONS
            elif not has_position and pos_count < max_positions:
                is_golden_cross = (prev_fast <= prev_slow and fast_ema > slow_ema) or (fast_ema > slow_ema and prev_fast < prev_slow)
                # Or sustained trend if golden cross happened and RSI is in target zone
                rsi_valid = rsi_val <= rsi_threshold

                if is_golden_cross and rsi_valid:
                    signal = "BUY"
                    reason = f"Golden Cross (EMA{fast_period} {fast_ema:.1f} > EMA{slow_period} {slow_ema:.1f}) & RSI {rsi_val:.1f} <= {rsi_threshold}"

                    # Capital allocation
                    allocable_cash = self.broker.get_portfolio_value() * max_alloc_pct
                    spend_cash = min(self.broker.cash, allocable_cash)
                    shares = int(spend_cash // (close_price * 1.001))

                    if shares > 0:
                        order_res = self.broker.execute_order(
                            symbol=sym_key,
                            side="BUY",
                            quantity=shares,
                            price=close_price,
                            order_type="market",
                            strategy_id=strategy.strategy_name,
                            rule_reason=f"Simulation Rule: {reason}",
                            timestamp_str=date_str
                        )
                        orders_triggered += 1
                    else:
                        reason += " (Insufficient cash to purchase minimum 1 share)"

            replay_journal.append({
                "step": i,
                "date": date_str,
                "close": close_price,
                "fast_ema": round(fast_ema, 2),
                "slow_ema": round(slow_ema, 2),
                "rsi": round(rsi_val, 2),
                "signal": signal,
                "reason": reason,
                "order_executed": bool(order_res and order_res.get("success")),
                "order_details": order_res,
                "cash": round(self.broker.cash, 2),
                "portfolio_value": round(self.broker.get_portfolio_value(), 2),
                "ml_prediction": ml_pred
            })

        self.broker.save_state()

        final_pv = self.broker.get_portfolio_value()
        net_pnl = final_pv - self.broker.initial_capital
        return_pct = (net_pnl / self.broker.initial_capital) * 100.0 if self.broker.initial_capital > 0 else 0.0

        # Persist simulation run metadata in MongoDB
        try:
            from quantlens.db_mongodb import get_mongodb
            from datetime import datetime
            import time
            db_mgr = get_mongodb()
            if db_mgr.is_connected():
                run_doc = {
                    "run_id": f"SIM-{int(time.time() * 1000) % 1000000:06d}",
                    "strategy_name": strategy.strategy_name,
                    "symbol": symbol,
                    "window_bars": len(replay_journal),
                    "start_date": replay_journal[0]["date"] if replay_journal else None,
                    "end_date": replay_journal[-1]["date"] if replay_journal else None,
                    "orders_triggered": orders_triggered,
                    "final_cash": round(self.broker.cash, 2),
                    "final_portfolio_value": round(final_pv, 2),
                    "total_pnl": round(net_pnl, 2),
                    "total_return_pct": round(return_pct, 2),
                    "executed_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                }
                db_mgr.db.paper_simulation_runs.insert_one(run_doc)
        except Exception as e:
            logger.warning(f"Failed to record simulation run in MongoDB: {e}")

        return {
            "status": "success",
            "symbol": symbol,
            "window_bars": len(replay_journal),
            "start_date": replay_journal[0]["date"] if replay_journal else None,
            "end_date": replay_journal[-1]["date"] if replay_journal else None,
            "orders_triggered": orders_triggered,
            "final_cash": round(self.broker.cash, 2),
            "final_portfolio_value": round(final_pv, 2),
            "total_pnl": round(net_pnl, 2),
            "total_return_pct": round(return_pct, 2),
            "journal": replay_journal,
            "dashboard_summary": self.broker.get_dashboard_summary()
        }
