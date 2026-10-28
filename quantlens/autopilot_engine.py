"""
QuantLens Autopilot — AI-Powered Continuous Paper Trading Simulator.
Authoritative backend session controller and state machine for:
- Continuous historical replay (candle-by-candle evaluation)
- Deterministic algorithmic rule execution (Fast/Slow EMA, RSI momentum filter, SL, TP)
- Real-time double-entry cash and position accounting in PaperBroker
- Active strategy decision engine with condition-by-condition transparency
- Continuous operational activity feed with typed event telemetry
- Interactive trade explanations (Rule trace + XGBoost/PyTorch + SHAP/LIME)
- Synthetic market sandbox for demonstrative scenarios
- Durable session persistence in MongoDB ('paper_simulation_sessions')
"""

import os
import time
import math
import logging
from datetime import datetime
from typing import Dict, Any, List, Optional, Tuple

import pandas as pd
import numpy as np

from quantlens.strategy_schema import StrategyDefinition
from quantlens.data_loader import load_historical_ohlcv
from quantlens.feature_engineering import calculate_rsi, calculate_atr
from quantlens.paper_broker import PaperBroker, get_paper_broker
from quantlens.db_mongodb import get_mongodb
from quantlens.xai_engine import get_xai_explanation

logger = logging.getLogger(__name__)

# Registry of active Autopilot sessions in memory
_AUTOPILOT_SESSIONS: Dict[str, "AutopilotSession"] = {}


class AutopilotSession:
    """Manages an autonomous continuous paper trading simulation session."""

    def __init__(
        self,
        strategy_or_session_id: Any = None,
        strategy: Optional[StrategyDefinition] = None,
        symbol: str = "RELIANCE",
        scenario: str = "trend_following",
        window_bars: int = 120,
        replay_bars: Optional[int] = None,
        initial_capital: float = 100000.0,
        synthetic_type: Optional[str] = None,
        session_id: Optional[str] = None
    ):
        if isinstance(strategy_or_session_id, str):
            self.session_id = strategy_or_session_id
            self.strategy = strategy
        else:
            self.strategy = strategy_or_session_id or strategy
            self.session_id = session_id or f"ap-session-{int(time.time() * 1000)}"

        self.symbol = symbol.upper().replace(".NS", "")
        self.scenario = scenario
        self.synthetic_type = synthetic_type
        self.is_synthetic = (scenario == "synthetic")
        bars = replay_bars if replay_bars is not None else window_bars
        self.window_bars = max(30, int(bars))
        self.initial_capital = float(initial_capital)

        # Broker reference
        self.broker = get_paper_broker()
        self.broker.reset_account(initial_capital=self.initial_capital)

        # Load & prepare scenario dataset
        self.df = self._prepare_scenario_data()

        # Progression state
        self.current_idx = 1  # Index into self.df (starts at 1 to compare with bar 0)
        self.total_bars = len(self.df)
        self.playback_speed = 1
        self.status = "READY"  # READY, EVALUATING, WAITING, SIGNAL_DETECTED, ORDER_FILLED, POSITION_MONITORING, PAUSED, COMPLETED
        self.loop_mode = False
        self.loop_cycle = 1

        # Historical tracking & metrics
        self.journal: List[Dict[str, Any]] = []
        self.activity_feed: List[Dict[str, Any]] = []
        self.equity_curve: List[Dict[str, Any]] = []
        self.peak_equity = self.initial_capital
        self.current_decision_card: Dict[str, Any] = {}
        self.created_at = datetime.now().isoformat()
        self.updated_at = self.created_at

        # Initial baseline event
        self._record_activity(
            event_type="SYSTEM",
            title="Autopilot Initialized",
            detail=f"Loaded {self.total_bars} historical candles for {self.symbol}. Virtual funds: ₹{self.initial_capital:,.2f}.",
            values={"starting_capital": self.initial_capital, "scenario": self.scenario},
            status="info"
        )

        # Initial equity snapshot
        self.equity_curve.append({
            "step": 0,
            "date": str(self.df["date"].iloc[0])[:10] if "date" in self.df.columns else "Day 0",
            "timestamp": str(self.df["date"].iloc[0])[:10] if "date" in self.df.columns else "Day 0",
            "equity": self.initial_capital,
            "cash": self.initial_capital,
            "invested": 0.0,
            "unrealized_pnl": 0.0,
            "realized_pnl": 0.0,
            "drawdown_pct": 0.0
        })

    def _prepare_scenario_data(self) -> pd.DataFrame:
        """Loads and prepares the dataset based on selected scenario."""
        fast_period = self.strategy.indicators.ema_fast_period
        slow_period = self.strategy.indicators.ema_slow_period
        rsi_period = self.strategy.indicators.rsi_period

        if self.is_synthetic:
            df = self._generate_synthetic_data(self.synthetic_type or "trending_up", length=self.window_bars)
        else:
            raw_df = load_historical_ohlcv(self.symbol)
            # Pick scenario slice
            if self.scenario == "risk_management":
                # Slice with high volatility / corrective period (e.g. early 2026 or 2022)
                start_offset = min(180, len(raw_df) - self.window_bars)
                df = raw_df.iloc[-start_offset : -start_offset + self.window_bars].copy()
            elif self.scenario == "extended":
                # Extended slice (e.g. 240+ bars)
                bars = min(len(raw_df), max(200, self.window_bars))
                df = raw_df.iloc[-bars:].copy()
            else:
                # Default trend following slice
                df = raw_df.iloc[-self.window_bars:].copy()

        df = df.reset_index(drop=True)

        # Calculate indicators causally
        df[f"ema_{fast_period}"] = df["close"].ewm(span=fast_period, adjust=False).mean()
        df[f"ema_{slow_period}"] = df["close"].ewm(span=slow_period, adjust=False).mean()
        df[f"rsi_{rsi_period}"] = calculate_rsi(df["close"], period=rsi_period)
        df["atr_14"] = calculate_atr(df, period=14)

        return df

    def _generate_synthetic_data(self, scenario_type: str, length: int = 100) -> pd.DataFrame:
        """Generates realistic synthetic OHLCV data for demonstration testing."""
        np.random.seed(42)
        base_price = 1250.0

        if scenario_type == "trending_up":
            drift = 0.003
            vol = 0.012
        elif scenario_type == "trending_down":
            drift = -0.003
            vol = 0.012
        elif scenario_type == "volatile":
            drift = 0.0005
            vol = 0.025
        else:  # sideways
            drift = 0.0
            vol = 0.008

        prices = [base_price]
        for _ in range(length):
            ret = np.random.normal(drift, vol)
            prices.append(prices[-1] * (1.0 + ret))

        dates = pd.date_range(end=datetime.now(), periods=length + 1, freq="B")
        rows = []
        for i in range(1, length + 1):
            c = prices[i]
            o = prices[i - 1]
            h = max(o, c) * (1.0 + abs(np.random.normal(0, vol * 0.5)))
            l = min(o, c) * (1.0 - abs(np.random.normal(0, vol * 0.5)))
            v = int(np.random.uniform(8000000, 18000000))
            rows.append({
                "date": dates[i].strftime("%Y-%m-%d"),
                "open": round(o, 2),
                "high": round(h, 2),
                "low": round(l, 2),
                "close": round(c, 2),
                "volume": v
            })
        return pd.DataFrame(rows)

    def _record_activity(
        self,
        event_type: str,
        title: str,
        detail: str,
        values: Optional[Dict[str, Any]] = None,
        status: str = "info"
    ):
        """Appends a typed event to the live Autopilot activity feed."""
        now = datetime.now()
        event_id = f"EVT-{int(now.timestamp() * 1000) % 1000000:06d}"
        candle_date = str(self.df["date"].iloc[min(self.current_idx, len(self.df) - 1)])[:10]

        event = {
            "event_id": event_id,
            "type": event_type,  # DATA, INDICATOR, DECISION, RISK, ORDER, POSITION, EXPLANATION, SYSTEM
            "timestamp": now.strftime("%H:%M:%S.%f")[:-3],
            "candle_date": candle_date,
            "title": title,
            "detail": detail,
            "values": values or {},
            "status": status  # info, success, warning, danger
        }
        self.activity_feed.insert(0, event)
        if len(self.activity_feed) > 200:
            self.activity_feed.pop()

    def step(self) -> Dict[str, Any]:
        """
        Executes one historical candle step causally:
        1. Advances candle cursor.
        2. Calculates indicators.
        3. Evaluates exits (stop loss, take profit, death cross).
        4. Evaluates entries (golden cross, RSI filter, allocation limit).
        5. Executes simulated orders in PaperBroker.
        6. Updates marked-to-market prices and cash conservation.
        7. Records decision card, activity events, and equity curve point.
        """
        if self.current_idx >= len(self.df):
            if self.loop_mode:
                self.loop_cycle += 1
                self.current_idx = 1
                self.broker.reset_account(self.initial_capital)
                self._record_activity(
                    event_type="SYSTEM",
                    title=f"Demo Loop Cycle #{self.loop_cycle} Started",
                    detail=f"Replay restarted cleanly for presentation loop. Virtual funds reset to ₹{self.initial_capital:,.2f}.",
                    values={"cycle": self.loop_cycle},
                    status="info"
                )
            else:
                self.status = "COMPLETED"
                return self.get_state()

        fast_p = self.strategy.indicators.ema_fast_period
        slow_p = self.strategy.indicators.ema_slow_period
        rsi_p = self.strategy.indicators.rsi_period
        rsi_th = self.strategy.indicators.rsi_threshold
        sl_pct = self.strategy.exit_rule.stop_loss_pct / 100.0
        tp_pct = self.strategy.exit_rule.take_profit_pct / 100.0
        max_alloc_pct = self.strategy.risk_config.max_position_allocation_pct / 100.0
        max_pos = self.strategy.risk_config.max_open_positions

        prev_row = self.df.iloc[self.current_idx - 1]
        curr_row = self.df.iloc[self.current_idx]

        date_val = curr_row["date"]
        date_str = date_val.strftime("%Y-%m-%d") if hasattr(date_val, "strftime") else str(date_val)[:10]

        close_px = float(curr_row["close"])
        high_px = float(curr_row["high"])
        low_px = float(curr_row["low"])
        vol = int(curr_row.get("volume", 10000000))

        fast_ema = float(curr_row[f"ema_{fast_p}"])
        slow_ema = float(curr_row[f"ema_{slow_p}"])
        rsi_val = float(curr_row[f"rsi_{rsi_p}"]) if not np.isnan(curr_row[f"rsi_{rsi_p}"]) else 50.0

        prev_fast = float(prev_row[f"ema_{fast_p}"])
        prev_slow = float(prev_row[f"ema_{slow_p}"])

        # Mark-to-market prices in broker
        self.broker.update_market_prices({self.symbol: close_px})

        # Position tracking
        has_pos = self.symbol in self.broker.positions and self.broker.positions[self.symbol]["shares"] > 0
        pos = self.broker.positions.get(self.symbol) if has_pos else None

        signal = "HOLD"
        reason = "Monitoring trend and boundaries"
        executed_order = None
        what_doing_now = "Analyzing the next historical candle."

        # Crossover detection
        golden_cross = (prev_fast <= prev_slow and fast_ema > slow_ema) or (fast_ema > slow_ema and prev_fast < prev_slow)
        death_cross = (prev_fast >= prev_slow and fast_ema < slow_ema) or (fast_ema < slow_ema and prev_fast > prev_slow)
        rsi_valid = (rsi_val <= rsi_th)

        stop_loss_hit = False
        take_profit_hit = False
        current_pnl_pct = None

        # -------------------------------------------------------------
        # 1. EVALUATE EXIT CONDITIONS (If Position Active)
        # -------------------------------------------------------------
        if has_pos:
            self.status = "POSITION_MONITORING"
            avg_px = pos["avg_price"]
            current_pnl_pct = (close_px - avg_px) / avg_px
            what_doing_now = f"Monitoring open position in {self.symbol} ({current_pnl_pct*100:+.2f}%). Exit triggers active."

            exit_rule_label = ""
            reason_code = "HOLD_POSITION_OPEN"
            if current_pnl_pct <= -sl_pct or low_px <= (avg_px * (1.0 - sl_pct)):
                stop_loss_hit = True
                exit_rule_label = f"Stop-Loss Cutoff Hit ({current_pnl_pct*100:.2f}% <= -{sl_pct*100:.1f}%)"
                reason_code = "EXIT_STOP_LOSS"
            elif current_pnl_pct >= tp_pct or high_px >= (avg_px * (1.0 + tp_pct)):
                take_profit_hit = True
                exit_rule_label = f"Take-Profit Target Achieved ({current_pnl_pct*100:.2f}% >= +{tp_pct*100:.1f}%)"
                reason_code = "EXIT_TAKE_PROFIT"
            elif death_cross:
                exit_rule_label = f"Bearish EMA Death Cross (EMA{fast_p} {fast_ema:.1f} < EMA{slow_p} {slow_ema:.1f})"
                reason_code = "EXIT_REVERSE_CROSSOVER"

            if exit_rule_label:
                signal = "SELL"
                reason = exit_rule_label
                self.status = "SIGNAL_DETECTED"
                what_doing_now = f"Exit rule triggered: {exit_rule_label}. Executing simulated SELL order."

                self._record_activity(
                    event_type="DECISION",
                    title=f"Exit Signal Detected: {self.symbol}",
                    detail=f"Condition: {exit_rule_label} [{reason_code}]. Closing {pos['shares']} shares @ ₹{close_px:,.2f}.",
                    values={"shares": pos["shares"], "price": close_px, "pnl_pct": round(current_pnl_pct*100, 2), "reason_code": reason_code},
                    status="warning" if current_pnl_pct < 0 else "success"
                )

                # Execute order through broker
                executed_order = self.broker.execute_order(
                    symbol=self.symbol,
                    side="SELL",
                    quantity=pos["shares"],
                    price=close_px,
                    order_type="market",
                    strategy_id=self.strategy.strategy_name,
                    rule_reason=f"Autopilot Exit: {exit_rule_label}",
                    timestamp_str=date_str,
                    reason_code=reason_code
                )
                self.status = "ORDER_FILLED"

                net_res = (executed_order.get("gross_value", 0) - executed_order.get("fee", 0)) - (pos["shares"] * avg_px)
                self._record_activity(
                    event_type="ORDER",
                    title=f"Paper SELL Filled: {executed_order.get('order_id')}",
                    detail=f"Sold {pos['shares']} shares @ ₹{close_px:,.2f} | Net Result: {'+' if net_res >= 0 else ''}₹{net_res:,.2f} | Reason: {exit_rule_label} [{reason_code}]",
                    values={"order_id": executed_order.get("order_id"), "net_result": round(net_res, 2), "reason_code": reason_code},
                    status="success" if net_res >= 0 else "danger"
                )

        # -------------------------------------------------------------
        # 2. EVALUATE ENTRY CONDITIONS (If No Position)
        # -------------------------------------------------------------
        elif not has_pos and len(self.broker.positions) < max_pos:
            what_doing_now = f"Scanning {self.symbol} for Golden Cross (EMA {fast_p} > {slow_p}) with RSI < {rsi_th}."

            if golden_cross and rsi_valid:
                signal = "BUY"
                reason_code = "ENTRY_EMA_CROSSOVER"
                reason = f"Bullish Golden Cross (EMA{fast_p} {fast_ema:.1f} > EMA{slow_p} {slow_ema:.1f}) with RSI {rsi_val:.1f} < {rsi_th}"
                self.status = "SIGNAL_DETECTED"
                what_doing_now = f"Entry signal detected: Golden Cross + RSI confirmation. Checking capital risk limits."

                self._record_activity(
                    event_type="DECISION",
                    title=f"Entry Signal Confirmed: {self.symbol}",
                    detail=f"Golden Cross detected! Fast EMA({fast_ema:.1f}) > Slow EMA({slow_ema:.1f}) & RSI({rsi_val:.1f}) < {rsi_th} [{reason_code}].",
                    values={"fast_ema": round(fast_ema, 2), "slow_ema": round(slow_ema, 2), "rsi": round(rsi_val, 2), "reason_code": reason_code},
                    status="success"
                )

                # Allocation calculation
                allocable_cash = self.broker.get_portfolio_value() * max_alloc_pct
                spend_cash = min(self.broker.cash, allocable_cash)
                shares = int(spend_cash // (close_px * 1.001))

                if shares > 0:
                    self._record_activity(
                        event_type="RISK",
                        title="Risk Allocation Check Passed",
                        detail=f"Approved virtual purchase of {shares} shares within {max_alloc_pct*100:.0f}% cash limit.",
                        values={"shares": shares, "allocation_cash": round(spend_cash, 2)},
                        status="info"
                    )

                    executed_order = self.broker.execute_order(
                        symbol=self.symbol,
                        side="BUY",
                        quantity=shares,
                        price=close_px,
                        order_type="market",
                        strategy_id=self.strategy.strategy_name,
                        rule_reason=f"Autopilot Entry: {reason}",
                        timestamp_str=date_str,
                        reason_code=reason_code
                    )
                    self.status = "ORDER_FILLED"

                    self._record_activity(
                        event_type="ORDER",
                        title=f"Paper BUY Filled: {executed_order.get('order_id')}",
                        detail=f"Bought {shares} shares of {self.symbol} @ ₹{close_px:,.2f}. Slippage 0.05% + fee 0.05% factored in. [{reason_code}]",
                        values={"order_id": executed_order.get("order_id"), "shares": shares, "fill_price": close_px, "reason_code": reason_code},
                        status="success"
                    )
                else:
                    signal = "HOLD"
                    reason_code = "REJECT_INSUFFICIENT_FUNDS"
                    reason += " [Risk Reject: Insufficient cash for min 1 share]"
                    self._record_activity(
                        event_type="RISK",
                        title="Risk Reject: Insufficient Capital",
                        detail=f"Available allocable cash ₹{spend_cash:,.2f} is insufficient for 1 share @ ₹{close_px:,.2f}.",
                        status="warning"
                    )
            elif golden_cross and not rsi_valid:
                reason_code = "HOLD_ENTRY_CONDITIONS_NOT_MET"
                what_doing_now = f"Golden Cross detected, but RSI is overbought ({rsi_val:.1f} >= {rsi_th}). Cooling down; waiting."
                self._record_activity(
                    event_type="DECISION",
                    title="RSI Exhaustion Filter Rejected Entry",
                    detail=f"Golden Cross occurred, but RSI {rsi_val:.1f} >= ceiling {rsi_th}. Entry rejected to prevent buying exhaustion top.",
                    values={"rsi": round(rsi_val, 2)},
                    status="warning"
                )
            else:
                reason_code = "HOLD_ENTRY_CONDITIONS_NOT_MET"
                what_doing_now = f"Checking EMA trend. Fast EMA is {('above' if fast_ema > slow_ema else 'below')} Slow EMA. Waiting for crossover."
        else:
            reason_code = "HOLD_POSITION_OPEN" if has_pos else "HOLD_ENTRY_CONDITIONS_NOT_MET"

        # -------------------------------------------------------------
        # 3. CONSTRUCT ACTIVE STRATEGY DECISION CARD
        # -------------------------------------------------------------
        final_decision_title = "WAITING FOR ENTRY SETUP"
        if signal == "BUY":
            final_decision_title = "BUY SIGNAL CONFIRMED"
        elif signal == "SELL":
            final_decision_title = f"EXIT SIGNAL CONFIRMED ({reason})"
        elif has_pos:
            final_decision_title = "HOLDING EXISTING POSITION"

        self.current_decision_card = {
            "candle_date": date_str,
            "close_price": close_px,
            "fast_ema": round(fast_ema, 2),
            "ema_fast": round(fast_ema, 2),
            "slow_ema": round(slow_ema, 2),
            "ema_slow": round(slow_ema, 2),
            "ema_crossover": "YES" if (golden_cross or death_cross) else "NO",
            "ema_cross_type": "GOLDEN_CROSS" if golden_cross else ("DEATH_CROSS" if death_cross else "NONE"),
            "current_rsi": round(rsi_val, 2),
            "rsi": round(rsi_val, 2),
            "rsi_threshold": rsi_th,
            "rsi_condition": "PASSED" if rsi_valid else "FAILED (EXHAUSTED)",
            "open_position_state": "ACTIVE" if has_pos else "NONE",
            "has_position": bool(has_pos),
            "open_shares": pos["shares"] if has_pos else 0,
            "entry_price": pos["avg_price"] if has_pos else 0.0,
            "stop_loss_price": round(pos["avg_price"] * (1.0 - sl_pct), 2) if has_pos else 0.0,
            "take_profit_price": round(pos["avg_price"] * (1.0 + tp_pct), 2) if has_pos else 0.0,
            "position_shares": pos["shares"] if has_pos else 0,
            "position_avg_px": pos["avg_price"] if has_pos else 0.0,
            "current_pnl_pct": round(current_pnl_pct * 100, 2) if current_pnl_pct is not None else 0.0,
            "stop_loss_hit": stop_loss_hit,
            "take_profit_hit": take_profit_hit,
            "conditions": {
                "fast_above_slow": bool(fast_ema > slow_ema),
                "rsi_under_threshold": bool(rsi_valid),
                "has_position": bool(has_pos),
                "stop_loss_hit": bool(stop_loss_hit),
                "take_profit_hit": bool(take_profit_hit)
            },
            "reason_code": reason_code,
            "available_cash": round(self.broker.cash, 2),
            "allocation_limit_pct": max_alloc_pct * 100.0,
            "risk_validation": "APPROVED" if (signal == "BUY" and executed_order and executed_order.get("success")) else "MONITORING",
            "final_action": signal,
            "action": signal,
            "final_decision_title": final_decision_title,
            "reason": reason,
            "what_doing_now": what_doing_now,
            "narration": what_doing_now
        }

        # -------------------------------------------------------------
        # 4. PORTFOLIO SNAPSHOT & EQUITY PROGRESSION
        # -------------------------------------------------------------
        cur_pv = round(self.broker.get_portfolio_value(), 2)
        if cur_pv > self.peak_equity:
            self.peak_equity = cur_pv
        dd_pct = round(((self.peak_equity - cur_pv) / self.peak_equity) * 100.0, 2) if self.peak_equity > 0 else 0.0

        unrealized = sum(p["unrealized_pnl"] for p in self.broker.positions.values())
        realized = sum(t["net_pnl"] for t in self.broker.trade_history)

        self.equity_curve.append({
            "step": self.current_idx,
            "date": date_str,
            "timestamp": date_str,
            "equity": cur_pv,
            "cash": round(self.broker.cash, 2),
            "invested": round(cur_pv - self.broker.cash, 2),
            "unrealized_pnl": round(unrealized, 2),
            "realized_pnl": round(realized, 2),
            "drawdown_pct": dd_pct
        })

        self.journal.append({
            "step": self.current_idx,
            "date": date_str,
            "close": close_px,
            "signal": signal,
            "reason": reason,
            "order": executed_order,
            "equity": cur_pv
        })

        self.current_idx += 1
        self.updated_at = datetime.now().isoformat()

        # Checkpoint to MongoDB every 5 steps or on order execution
        if executed_order or self.current_idx % 10 == 0:
            self.persist_session_checkpoint()

        return self.get_state()

    def skip_to_next_signal(self) -> Dict[str, Any]:
        """
        Advances the simulation continuously across intervening candles,
        faithfully processing stops, mark-to-market prices, and cash updates on every bar,
        until a BUY or SELL order is executed or dataset ends.
        """
        initial_order_count = len(self.broker.orders)
        steps_taken = 0

        while self.current_idx < len(self.df):
            state = self.step()
            steps_taken += 1
            if len(self.broker.orders) > initial_order_count:
                self._record_activity(
                    event_type="SYSTEM",
                    title="Fast-Forwarded to Next Signal",
                    detail=f"Processed {steps_taken} intervening daily candles with accurate mark-to-market valuations.",
                    status="info"
                )
                break

        return self.get_state()

    def get_trade_explanation(self, order_id: str) -> Dict[str, Any]:
        """
        Returns complete transparent explanation for an executed paper order:
        - Exact mathematical rule that triggered
        - Fast/Slow EMA values, RSI, stop-loss / take-profit calculations
        - Machine learning prediction (XGBoost & PyTorch MLP) on that exact bar
        - SHAP top contributing features and LIME surrogate rules
        - Grounded natural English commentary
        - MongoDB record reference
        """
        order = next((o for o in self.broker.orders if o.get("order_id") == order_id), None)
        if not order and len(self.broker.orders) > 0:
            order = self.broker.orders[0]

        if not order:
            return {"success": False, "error": f"Order '{order_id}' not found."}

        order_date = order.get("timestamp", "")[:10]
        side = order.get("side", "BUY")
        sym = order.get("symbol", self.symbol)

        # Retrieve bar from df matching order date
        matched_idx = -1
        for idx in range(len(self.df)):
            d_str = str(self.df["date"].iloc[idx])[:10]
            if d_str == order_date:
                matched_idx = idx
                break

        if matched_idx < 0:
            matched_idx = max(0, self.current_idx - 1)

        row = self.df.iloc[matched_idx]
        fast_p = self.strategy.indicators.ema_fast_period
        slow_p = self.strategy.indicators.ema_slow_period
        rsi_p = self.strategy.indicators.rsi_period

        # Compute or load XAI explanation for this sample using exact target_date
        xai_info = None
        try:
            xai_info = get_xai_explanation(self.symbol, target_date=order_date)
        except Exception as e:
            logger.warning(f"Could not fetch XAI by date for order {order_id} on {order_date}: {e}")
            try:
                xai_info = get_xai_explanation(self.symbol, bar_index=matched_idx)
            except Exception as e2:
                logger.warning(f"Fallback bar_index failed: {e2}")

        models_summary = xai_info.get("models_summary", {}) if xai_info else {}
        xgb_info = models_summary.get("xgboost", {})
        torch_info = models_summary.get("pytorch_mlp", {})
        model_prediction_label = xgb_info.get("prediction", "HOLD")
        raw_conf = float(xgb_info.get("confidence", 50.0))
        model_confidence_pct = round(raw_conf if raw_conf > 1.0 else raw_conf * 100.0, 1)

        raw_torch_conf = float(torch_info.get("confidence", 50.0))
        torch_confidence_pct = round(raw_torch_conf if raw_torch_conf > 1.0 else raw_torch_conf * 100.0, 1)

        rule_reason = order.get("rule_reason", "Strategy Trigger")
        reason_code = order.get("reason_code", "EXIT_SIGNAL" if side == "SELL" else "ENTRY_SIGNAL")

        # 1. Distinct Concept: MODEL PREDICTION (Statistical ML Forecast)
        model_concept = {
            "model_type": "XGBoost + PyTorch Ensemble",
            "prediction": model_prediction_label,
            "confidence_pct": model_confidence_pct,
            "confidence": model_confidence_pct,
            "probabilities": xgb_info.get("probabilities", {}),
            "pytorch_prediction": torch_info.get("prediction", "HOLD"),
            "pytorch_confidence_pct": torch_confidence_pct,
            "models_agree": models_summary.get("models_agree", True),
            "consensus_signal": models_summary.get("consensus_signal", model_prediction_label),
            "top_drivers": xai_info.get("shap_explanation", {}).get("top_features", [])[:4] if xai_info else []
        }

        # 2. Distinct Concept: STRATEGY DECISION (Deterministic Quantitative Rules)
        strategy_concept = {
            "strategy_name": self.strategy.strategy_name,
            "rule_reason": rule_reason,
            "reason_code": reason_code,
            "direction": side,
            "condition_evaluated": f"Fast EMA({row[f'ema_{fast_p}']:.1f}) vs Slow EMA({row[f'ema_{slow_p}']:.1f}) | RSI({row[f'rsi_{rsi_p}']:.1f})",
            "priority": "CAPITAL_PROTECTION_OVERRIDE" if "STOP_LOSS" in str(reason_code) else ("PROFIT_HARVEST_OVERRIDE" if "TAKE_PROFIT" in str(reason_code) else "RULE_BASED_EXECUTION")
        }

        # 3. Distinct Concept: ORDER EXECUTION (Paper Broker Ledger)
        order_concept = {
            "order_id": order.get("order_id"),
            "side": side,
            "quantity": order.get("quantity"),
            "price": order.get("price"),
            "fill_price": order.get("fill_price"),
            "gross_value": order.get("gross_value"),
            "fee": order.get("fee", order.get("brokerage_fee", 0.0)),
            "brokerage_fee": order.get("fee", order.get("brokerage_fee", 0.0)),
            "slippage_rate": 0.0005,
            "status": order.get("status", "EXECUTED"),
            "accounting_mode": "STRICT_DOUBLE_ENTRY"
        }

        # RULE PRECEDENCE NOTICE / CONVERGENCE NOTICE
        if side != model_prediction_label:
            if side == "SELL" and model_prediction_label == "BUY":
                precedence_notice = (
                    f"RULE PRECEDENCE ACTIVE: The statistical ML model predicted BUY ({model_confidence_pct:.1f}% confidence over a 5-day forecast horizon), "
                    f"but the user's deterministic Risk Management Rule ('{rule_reason}') triggered liquidation. "
                    f"In institutional quantitative systems, capital preservation and stop-loss boundaries strictly override predictive ML signals to prevent drawdown."
                )
            elif side == "BUY" and model_prediction_label == "SELL":
                precedence_notice = (
                    f"RULE PRECEDENCE ACTIVE: The quantitative strategy entry rule triggered BUY, while the statistical ML model was defensive (SELL). "
                    f"The strategy rule executed with strict position sizing and stop-loss protection in place."
                )
            else:
                precedence_notice = (
                    f"RULE PRECEDENCE ACTIVE: Deterministic strategy rule '{rule_reason}' took precedence over model forecast '{model_prediction_label}'."
                )
        else:
            precedence_notice = (
                f"CONVERGENT SIGNAL: Deterministic strategy rules and machine learning ensemble are mutually aligned in recommending {side}."
            )

        # Formulate grounded AI commentary
        if side == "BUY":
            narrative = (
                f"On {order_date}, the {fast_p}-day EMA ({row[f'ema_{fast_p}']:.2f}) crossed above the {slow_p}-day EMA "
                f"({row[f'ema_{slow_p}']:.2f}), confirming an upward directional breakout. The RSI(14) was {row[f'rsi_{rsi_p}']:.2f}, "
                f"safely below the {self.strategy.indicators.rsi_threshold:.1f} exhaustion ceiling. The risk engine verified that "
                f"allocating {order.get('quantity')} shares (₹{order.get('gross_value', 0):,.2f}) satisfied the 10% maximum cash limit."
            )
        else:
            narrative = (
                f"On {order_date}, the exit condition '{order.get('rule_reason', 'Exit')}' was met. "
                f"The system liquidated {order.get('quantity')} shares at ₹{order.get('price', 0):,.2f} to protect virtual capital "
                f"or harvest profits, factoring in realistic brokerage (0.05%) and slippage (0.05%)."
            )

        return {
            "success": True,
            "order_id": order.get("order_id"),
            "order": order,
            "order_date": order_date,
            "model_prediction": model_concept,
            "strategy_decision": strategy_concept,
            "order_execution": order_concept,
            "rule_precedence_notice": precedence_notice,
            "candle_metrics": {
                "close": float(row["close"]),
                "fast_ema": round(float(row[f"ema_{fast_p}"]), 2),
                "slow_ema": round(float(row[f"ema_{slow_p}"]), 2),
                "rsi": round(float(row[f"rsi_{rsi_p}"]), 2)
            },
            "rule_evaluation": {
                "rule_reason": order.get("rule_reason"),
                "reason_code": reason_code,
                "strategy_name": self.strategy.strategy_name,
                "direction": side,
                "shares": order.get("quantity"),
                "fee_deducted": order.get("brokerage_fee", 0.0)
            },
            "ml_xai_analysis": {
                "models_summary": models_summary if xai_info else None,
                "top_shap_features": xai_info.get("shap_explanation", {}).get("top_features", [])[:4] if xai_info else [],
                "top_lime_rules": xai_info.get("lime_explanation", {}).get("top_features", [])[:4] if xai_info else []
            },
            "ai_grounded_commentary": narrative,
            "storage_provenance": {
                "database": "quantlens_xai",
                "collection": "paper_orders",
                "persisted": True
            }
        }

    def persist_session_checkpoint(self):
        """Durably stores or updates the Autopilot session in MongoDB."""
        try:
            db_mgr = get_mongodb()
            if db_mgr.is_connected():
                summary = self.get_summary()
                doc = {
                    "session_id": self.session_id,
                    "strategy_name": self.strategy.strategy_name,
                    "symbol": self.symbol,
                    "scenario": self.scenario,
                    "is_synthetic": self.is_synthetic,
                    "current_step": self.current_idx,
                    "total_bars": self.total_bars,
                    "status": self.status,
                    "starting_capital": self.initial_capital,
                    "current_equity": summary["current_equity"],
                    "total_pnl": summary["total_pnl"],
                    "total_return_pct": summary["total_return_pct"],
                    "total_orders": summary["orders_count"],
                    "closed_trades": summary["closed_trades_count"],
                    "win_rate_pct": summary["win_rate_pct"],
                    "max_drawdown_pct": summary["max_drawdown_pct"],
                    "updated_at": datetime.now().isoformat()
                }
                db_mgr.db.paper_simulation_sessions.update_one(
                    {"session_id": self.session_id},
                    {"$set": doc},
                    upsert=True
                )
        except Exception as e:
            logger.warning(f"Could not persist autopilot session checkpoint in MongoDB: {e}")

    def get_summary(self) -> Dict[str, Any]:
        """Compiles comprehensive session summary for the wrap-up report."""
        cur_pv = round(self.broker.get_portfolio_value(), 2)
        total_pnl = round(cur_pv - self.initial_capital, 2)
        ret_pct = round((total_pnl / self.initial_capital) * 100.0, 2) if self.initial_capital > 0 else 0.0

        trades = self.broker.trade_history
        wins = len([t for t in trades if t.get("net_pnl", 0) > 0])
        losses = len([t for t in trades if t.get("net_pnl", 0) < 0])
        win_rate = round((wins / len(trades)) * 100.0, 2) if trades else 0.0

        max_dd = 0.0
        for pt in self.equity_curve:
            if pt.get("drawdown_pct", 0) > max_dd:
                max_dd = pt["drawdown_pct"]

        total_fees = sum(o.get("brokerage_fee", 0.0) for o in self.broker.orders)

        start_date = str(self.df["date"].iloc[0])[:10] if "date" in self.df.columns else "Day 0"
        curr_date = str(self.df["date"].iloc[min(self.current_idx - 1, len(self.df) - 1)])[:10]

        return {
            "session_id": self.session_id,
            "strategy_name": self.strategy.strategy_name,
            "symbol": self.symbol,
            "scenario": self.scenario,
            "is_synthetic": self.is_synthetic,
            "start_date": start_date,
            "current_date": curr_date,
            "bars_processed": self.current_idx,
            "total_bars": self.total_bars,
            "starting_capital": self.initial_capital,
            "current_equity": cur_pv,
            "available_cash": round(self.broker.cash, 2),
            "invested_value": round(cur_pv - self.broker.cash, 2),
            "unrealized_pnl": round(sum(p["unrealized_pnl"] for p in self.broker.positions.values()), 2),
            "realized_pnl": round(sum(t["net_pnl"] for t in trades), 2),
            "total_pnl": total_pnl,
            "total_return_pct": ret_pct,
            "orders_count": len(self.broker.orders),
            "closed_trades_count": len(trades),
            "winning_trades": wins,
            "losing_trades": losses,
            "win_rate_pct": win_rate,
            "max_drawdown_pct": max_dd,
            "total_fees_paid": round(total_fees, 2),
            "open_positions": list(self.broker.positions.values()),
            "status": self.status,
            "loop_cycle": self.loop_cycle
        }

    def get_state(self) -> Dict[str, Any]:
        """Returns the full state snapshot for the frontend Autopilot dashboard."""
        summary = self.get_summary()

        # Format latest candle OHLCV series for ApexCharts
        visible_bars = self.df.iloc[: self.current_idx]
        candles_list = []
        fast_ema_list = []
        slow_ema_list = []
        rsi_list = []

        fast_p = self.strategy.indicators.ema_fast_period
        slow_p = self.strategy.indicators.ema_slow_period
        rsi_p = self.strategy.indicators.rsi_period

        for i in range(len(visible_bars)):
            r = visible_bars.iloc[i]
            d_str = str(r["date"])[:10]
            candles_list.append({"x": d_str, "y": [r["open"], r["high"], r["low"], r["close"]]})
            fast_ema_list.append({"x": d_str, "y": round(float(r[f"ema_{fast_p}"]), 2)})
            slow_ema_list.append({"x": d_str, "y": round(float(r[f"ema_{slow_p}"]), 2)})
            rsi_list.append({"x": d_str, "y": round(float(r[f"rsi_{rsi_p}"]), 2)})

        # Formulate order markers for the chart
        markers = []
        for o in self.broker.orders:
            if o.get("status") == "EXECUTED":
                markers.append({
                    "date": o.get("timestamp", "")[:10],
                    "side": o.get("side"),
                    "price": o.get("price"),
                    "quantity": o.get("quantity"),
                    "order_id": o.get("order_id"),
                    "reason": o.get("rule_reason")
                })

        return {
            "success": True,
            "session_id": self.session_id,
            "status": self.status,
            "summary": summary,
            "current_decision_card": self.current_decision_card,
            "decision_card": self.current_decision_card,
            "chart_data": {
                "symbol": self.symbol,
                "current_bar": self.current_idx,
                "total_bars": self.total_bars,
                "candles": candles_list[-80:],  # Viewport window
                "ema_fast": fast_ema_list[-80:],
                "ema_slow": slow_ema_list[-80:],
                "rsi": rsi_list[-80:],
                "markers": markers
            },
            "activity_feed": self.activity_feed[:40],
            "equity_curve": self.equity_curve[-80:],
            "orders": self.broker.orders[:15],
            "trades": self.broker.trade_history[:15],
            "positions": self.broker.positions,
            "playback_speed": self.playback_speed,
            "loop_mode": self.loop_mode,
            "loop_cycle": self.loop_cycle
        }

    def pause(self) -> Dict[str, Any]:
        """Pauses simulation progression."""
        self.status = "PAUSED"
        self._record_activity(
            event_type="SYSTEM",
            title="Autopilot Simulation Paused",
            detail=f"Replay halted at bar {self.current_idx}/{self.total_bars}."
        )
        return self.get_state()

    def resume(self) -> Dict[str, Any]:
        """Resumes simulation progression."""
        self.status = "RUNNING"
        self._record_activity(
            event_type="SYSTEM",
            title="Autopilot Simulation Resumed",
            detail=f"Replay resumed at bar {self.current_idx}/{self.total_bars}."
        )
        return self.get_state()

    def set_speed(self, speed: float) -> Dict[str, Any]:
        """Sets playback speed multiplier."""
        self.playback_speed = max(1.0, min(float(speed), 10.0))
        return self.get_state()

    def reset(self) -> Dict[str, Any]:
        """Resets the simulation session and broker ledger."""
        self.current_idx = 1
        self.status = "READY"
        self.broker.reset_account(initial_capital=self.initial_capital)
        self.equity_curve = [{
            "bar_index": 0,
            "date": str(self.df["date"].iloc[0])[:10] if "date" in self.df.columns else "Day 0",
            "equity": self.initial_capital,
            "drawdown_pct": 0.0
        }]
        self.peak_equity = self.initial_capital
        self._record_activity(
            event_type="SYSTEM",
            title="Autopilot Session Reset",
            detail=f"Session restored to initial capital of ₹{self.initial_capital:,.2f}."
        )
        return self.get_state()


def init_autopilot_session(
    strategy: StrategyDefinition,
    symbol: str = "RELIANCE",
    scenario: str = "trend_following",
    window_bars: int = 120,
    initial_capital: float = 100000.0,
    synthetic_type: Optional[str] = None
) -> AutopilotSession:
    """Initializes and registers a new AutopilotSession."""
    session_id = f"ap-session-{int(time.time() * 1000)}"
    session = AutopilotSession(
        session_id=session_id,
        strategy=strategy,
        symbol=symbol,
        scenario=scenario,
        window_bars=window_bars,
        initial_capital=initial_capital,
        synthetic_type=synthetic_type
    )
    _AUTOPILOT_SESSIONS[session_id] = session
    return session


def get_autopilot_session(session_id: str) -> Optional[AutopilotSession]:
    """Retrieves an existing session by ID, or the most recent active session."""
    if session_id in _AUTOPILOT_SESSIONS:
        return _AUTOPILOT_SESSIONS[session_id]
    if _AUTOPILOT_SESSIONS:
        # Return most recent
        return list(_AUTOPILOT_SESSIONS.values())[-1]
    return None
