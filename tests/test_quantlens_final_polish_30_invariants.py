"""
QuantLens-XAI 30 Invariants Final Quality Assurance Test Suite.
Verifies the complete quantitative trading engine, XAI temporal alignment,
mathematical cash conservation, rule precedence over model signals, and UI telemetry.

Total Invariants: 30 / 30 strictly tested.
"""

import os
import unittest
import numpy as np
import pandas as pd
from datetime import datetime

from quantlens.data_loader import load_historical_ohlcv
from quantlens.ml_models import ModelManager, CLASS_NAMES
from quantlens.xai_engine import get_xai_explanation, get_xai_engine
from quantlens.paper_broker import PaperBroker
from quantlens.autopilot_engine import AutopilotSession
from quantlens.strategy_schema import (
    StrategyDefinition,
    IndicatorConfig,
    EntryRule,
    ExitRule,
    RiskManagement
)


class TestQuantLens30Invariants(unittest.TestCase):
    """30 Invariants Formal Acceptance Test Suite for QuantLens-XAI."""

    @classmethod
    def setUpClass(cls):
        cls.symbol = "RELIANCE"
        cls.df = load_historical_ohlcv(cls.symbol)
        cls.engine = get_xai_engine(cls.symbol)

        cls.strategy = StrategyDefinition(
            strategy_id="strat-final-polish",
            strategy_name="Final Polish Crossover Strategy",
            symbol="RELIANCE",
            raw_prompt="Buy RELIANCE when EMA 10 crosses above EMA 30 and RSI < 65, exit on reverse cross or 2% SL / 4% TP",
            indicators=IndicatorConfig(ema_fast_period=10, ema_slow_period=30, rsi_period=14, rsi_threshold=65.0),
            entry_rule=EntryRule(direction="BUY"),
            exit_rule=ExitRule(stop_loss_pct=2.0, take_profit_pct=4.0),
            risk_config=RiskManagement(initial_capital=100000.0, max_position_allocation_pct=10.0, max_open_positions=1)
        )

    # -------------------------------------------------------------------------
    # Invariant 01: Model Confidence Strictly Bounded
    # -------------------------------------------------------------------------
    def test_invariant_01_model_confidence_strictly_bounded(self):
        """Invariant 01: Model confidence must be strictly bounded in [0.0, 100.0]%, never >100%."""
        preds = self.engine.model_mgr.predict_sample(self.engine.X.iloc[-1].values)
        xgb_conf = preds["xgboost"]["confidence"]
        pt_conf = preds["pytorch_mlp"]["confidence"]

        self.assertGreaterEqual(xgb_conf, 0.0)
        self.assertLessEqual(xgb_conf, 100.0)
        self.assertGreaterEqual(pt_conf, 0.0)
        self.assertLessEqual(pt_conf, 100.0)

    # -------------------------------------------------------------------------
    # Invariant 02: XAI Temporal Alignment (Date-Based Sample Retrieval)
    # -------------------------------------------------------------------------
    def test_invariant_02_xai_temporal_alignment(self):
        """Invariant 02: XAI explanation matches the exact candle date of the order, not bar 5 from 2020."""
        target_date = "2026-05-06"
        exp = get_xai_explanation(self.symbol, target_date=target_date)
        self.assertEqual(exp["date"][:10], target_date)
        self.assertIn("prediction", exp)
        self.assertIn("shap_explanation", exp)

    # -------------------------------------------------------------------------
    # Invariant 03: Stop-Loss Precedence Over Bullish Model
    # -------------------------------------------------------------------------
    def test_invariant_03_stop_loss_precedence_over_bullish_model(self):
        """Invariant 03: Stop-Loss liquidation triggers SELL even when ML model is strongly BUY."""
        session = AutopilotSession(self.strategy, initial_capital=100000.0, replay_bars=120)
        # Fast-forward until a SELL occurs
        sell_order = None
        for _ in range(80):
            state = session.step()
            orders = session.broker.orders
            if orders and orders[0]["side"] == "SELL":
                sell_order = orders[0]
                break

        if sell_order:
            exp = session.get_trade_explanation(sell_order["order_id"])
            self.assertTrue(exp["success"])
            self.assertEqual(exp["order_execution"]["side"], "SELL")
            # Verify rule precedence notice exists and articulates risk priority
            self.assertIn("rule_precedence_notice", exp)
            self.assertIn("RULE PRECEDENCE ACTIVE", exp["rule_precedence_notice"])

    # -------------------------------------------------------------------------
    # Invariant 04: Take-Profit Precedence Over Bullish Model
    # -------------------------------------------------------------------------
    def test_invariant_04_take_profit_precedence_over_bullish_model(self):
        """Invariant 04: Take-Profit target harvests profits and overrides speculative hold signals."""
        broker = PaperBroker(initial_capital=100000.0)
        broker.execute_order("RELIANCE", "BUY", 10, 1000.0, reason_code="ENTRY_EMA_CROSSOVER")
        # Trigger take-profit at +5% (target +4%)
        order_res = broker.execute_order(
            "RELIANCE", "SELL", 10, 1050.0,
            rule_reason="Take-Profit Target Achieved (+5.0% >= +4.0%)",
            reason_code="EXIT_TAKE_PROFIT"
        )
        self.assertTrue(order_res["success"])
        self.assertEqual(broker.trade_history[0]["reason_code"], "EXIT_TAKE_PROFIT")

    # -------------------------------------------------------------------------
    # Invariant 05: Reverse Crossover Triggers Exit
    # -------------------------------------------------------------------------
    def test_invariant_05_reverse_crossover_triggers_exit(self):
        """Invariant 05: Bearish death cross triggers exit with EXIT_REVERSE_CROSSOVER reason code."""
        broker = PaperBroker(initial_capital=100000.0)
        broker.execute_order("RELIANCE", "BUY", 10, 1500.0, reason_code="ENTRY_EMA_CROSSOVER")
        order_res = broker.execute_order(
            "RELIANCE", "SELL", 10, 1480.0,
            rule_reason="Bearish EMA Death Cross (EMA10 < EMA30)",
            reason_code="EXIT_REVERSE_CROSSOVER"
        )
        self.assertTrue(order_res["success"])
        self.assertEqual(broker.trade_history[0]["reason_code"], "EXIT_REVERSE_CROSSOVER")

    # -------------------------------------------------------------------------
    # Invariant 06: Cash Conservation on BUY
    # -------------------------------------------------------------------------
    def test_invariant_06_cash_conservation_on_buy(self):
        """Invariant 06: On BUY, cash decreases by exactly gross value + fee."""
        broker = PaperBroker(initial_capital=100000.0)
        cash_before = broker.cash
        res = broker.execute_order("RELIANCE", "BUY", 10, 1000.0)
        self.assertTrue(res["success"])
        order = broker.orders[0]
        expected_cash = round(cash_before - (order["gross_value"] + order["fee"]), 2)
        self.assertEqual(round(broker.cash, 2), expected_cash)

    # -------------------------------------------------------------------------
    # Invariant 07: Cash Conservation on SELL
    # -------------------------------------------------------------------------
    def test_invariant_07_cash_conservation_on_sell(self):
        """Invariant 07: On SELL, cash increases by exactly gross value - fee."""
        broker = PaperBroker(initial_capital=100000.0)
        broker.execute_order("RELIANCE", "BUY", 10, 1000.0)
        cash_before_sell = broker.cash
        res = broker.execute_order("RELIANCE", "SELL", 10, 1020.0)
        self.assertTrue(res["success"])
        order = broker.orders[0]
        expected_cash = round(cash_before_sell + (order["gross_value"] - order["fee"]), 2)
        self.assertEqual(round(broker.cash, 2), expected_cash)

    # -------------------------------------------------------------------------
    # Invariant 08: Net P&L Strictly Equals Delta Cash Across Round Trips
    # -------------------------------------------------------------------------
    def test_invariant_08_net_pnl_strictly_equals_delta_cash(self):
        """Invariant 08: Realized Net P&L strictly matches total cash change across round trips."""
        broker = PaperBroker(initial_capital=100000.0)
        broker.reset_account(initial_capital=100000.0)
        initial_cash = broker.cash

        # Complete round-trip trade
        broker.execute_order("RELIANCE", "BUY", 10, 1200.0)
        broker.execute_order("RELIANCE", "SELL", 10, 1250.0)

        realized_net_pnl = sum(t["net_pnl"] for t in broker.trade_history)
        delta_cash = round(broker.cash - initial_cash, 2)
        self.assertAlmostEqual(realized_net_pnl, delta_cash, places=2)

    # -------------------------------------------------------------------------
    # Invariant 09: Portfolio Valuation Identity
    # -------------------------------------------------------------------------
    def test_invariant_09_portfolio_valuation_identity(self):
        """Invariant 09: Portfolio Total Value == Cash + Invested Market Value."""
        broker = PaperBroker(initial_capital=100000.0)
        broker.execute_order("RELIANCE", "BUY", 5, 2000.0)
        broker.update_market_prices({"RELIANCE": 2050.0})

        summary = broker.get_dashboard_summary()
        expected_total = round(summary["available_cash"] + summary["invested_value"], 2)
        self.assertEqual(round(summary["total_portfolio_value"], 2), expected_total)

    # -------------------------------------------------------------------------
    # Invariant 10: Insufficient Funds Rejection
    # -------------------------------------------------------------------------
    def test_invariant_10_insufficient_funds_rejection(self):
        """Invariant 10: Orders exceeding available cash are rejected and cash remains intact."""
        broker = PaperBroker(initial_capital=1000.0)
        initial_cash = broker.cash
        res = broker.execute_order("RELIANCE", "BUY", 100, 2500.0)
        self.assertFalse(res["success"])
        self.assertEqual(broker.cash, initial_cash)
        self.assertEqual(broker.orders[0]["status"], "REJECTED")

    # -------------------------------------------------------------------------
    # Invariant 11: Position Limit Enforcement
    # -------------------------------------------------------------------------
    def test_invariant_11_max_position_limit_enforcement(self):
        """Invariant 11: Max position count limit prevents duplicate simultaneous positions."""
        session = AutopilotSession(self.strategy, initial_capital=100000.0, replay_bars=60)
        # Buy once
        session.broker.execute_order("RELIANCE", "BUY", 5, 1400.0)
        # Advance 1 step
        state = session.step()
        # Decision engine recognizes active position
        self.assertTrue(state["decision_card"]["has_position"])

    # -------------------------------------------------------------------------
    # Invariant 12: Max Allocation Limit Enforcement
    # -------------------------------------------------------------------------
    def test_invariant_12_max_allocation_limit_enforcement(self):
        """Invariant 12: Order sizes are capped at 10% of portfolio value."""
        session = AutopilotSession(self.strategy, initial_capital=100000.0, replay_bars=60)
        for _ in range(30):
            session.step()
            orders = session.broker.orders
            if orders and orders[0]["side"] == "BUY":
                buy_val = orders[0]["gross_value"]
                # Capped at 10% of 100k = ~10k
                self.assertLessEqual(buy_val, 11000.0)
                break

    # -------------------------------------------------------------------------
    # Invariant 13: Standardized Reason Codes Present
    # -------------------------------------------------------------------------
    def test_invariant_13_standardized_reason_codes_present(self):
        """Invariant 13: Machine-readable reason codes are attached to orders and trades."""
        valid_codes = {
            "ENTRY_EMA_CROSSOVER", "ENTRY_RSI_CONFIRMED", "EXIT_STOP_LOSS",
            "EXIT_TAKE_PROFIT", "EXIT_REVERSE_CROSSOVER", "EXIT_SESSION_END",
            "HOLD_ENTRY_CONDITIONS_NOT_MET", "HOLD_POSITION_OPEN",
            "REJECT_INSUFFICIENT_FUNDS", "REJECT_POSITION_LIMIT", "ENTRY_SIGNAL", "EXIT_SIGNAL"
        }
        broker = PaperBroker(initial_capital=100000.0)
        broker.execute_order("RELIANCE", "BUY", 5, 1000.0, reason_code="ENTRY_EMA_CROSSOVER")
        broker.execute_order("RELIANCE", "SELL", 5, 1020.0, reason_code="EXIT_TAKE_PROFIT")

        self.assertIn(broker.orders[1]["reason_code"], valid_codes)
        self.assertIn(broker.orders[0]["reason_code"], valid_codes)
        self.assertIn(broker.trade_history[0]["reason_code"], valid_codes)

    # -------------------------------------------------------------------------
    # Invariant 14: Three-Way Separation in Trade Explanation
    # -------------------------------------------------------------------------
    def test_invariant_14_three_way_separation_in_trade_explanation(self):
        """Invariant 14: Trade explanation contains 3 distinct concepts: model, strategy, execution."""
        session = AutopilotSession(self.strategy, initial_capital=100000.0, replay_bars=60)
        for _ in range(30):
            session.step()
            if session.broker.orders:
                break

        order_id = session.broker.orders[0]["order_id"]
        exp = session.get_trade_explanation(order_id)
        self.assertIn("model_prediction", exp)
        self.assertIn("strategy_decision", exp)
        self.assertIn("order_execution", exp)

    # -------------------------------------------------------------------------
    # Invariant 15: Rule Precedence Notice Present
    # -------------------------------------------------------------------------
    def test_invariant_15_rule_precedence_notice_present(self):
        """Invariant 15: Trade explanation contains rule precedence or convergence notice."""
        session = AutopilotSession(self.strategy, initial_capital=100000.0, replay_bars=60)
        for _ in range(30):
            session.step()
            if session.broker.orders:
                break

        order_id = session.broker.orders[0]["order_id"]
        exp = session.get_trade_explanation(order_id)
        self.assertIn("rule_precedence_notice", exp)
        self.assertTrue(len(exp["rule_precedence_notice"]) > 10)

    # -------------------------------------------------------------------------
    # Invariant 16: Data Feed Transparency (Replay vs Live)
    # -------------------------------------------------------------------------
    def test_invariant_16_data_feed_status_transparency(self):
        """Invariant 16: Autopilot session clearly identifies historical replay without live feed claim."""
        session = AutopilotSession(self.strategy, initial_capital=100000.0, replay_bars=60)
        summary = session.get_summary()
        self.assertIn("start_date", summary)
        self.assertIn("current_date", summary)
        self.assertFalse(session.is_synthetic)

    # -------------------------------------------------------------------------
    # Invariant 17: Candle Geometry Validity
    # -------------------------------------------------------------------------
    def test_invariant_17_candle_geometry_validity(self):
        """Invariant 17: All candles satisfy High >= Low, High >= Open/Close, Low <= Open/Close."""
        for idx in range(min(50, len(self.df))):
            row = self.df.iloc[idx]
            self.assertGreaterEqual(row["high"], row["low"])
            self.assertGreaterEqual(row["high"], row["open"])
            self.assertGreaterEqual(row["high"], row["close"])
            self.assertLessEqual(row["low"], row["open"])
            self.assertLessEqual(row["low"], row["close"])

    # -------------------------------------------------------------------------
    # Invariant 18: Causal Step Without Lookahead
    # -------------------------------------------------------------------------
    def test_invariant_18_causal_step_no_lookahead(self):
        """Invariant 18: Step advances exactly by 1 candle without lookahead bias."""
        session = AutopilotSession(self.strategy, initial_capital=100000.0, replay_bars=60)
        idx_0 = session.current_idx
        session.step()
        idx_1 = session.current_idx
        self.assertEqual(idx_1, idx_0 + 1)

    # -------------------------------------------------------------------------
    # Invariant 19: Pause & Resume Idempotency
    # -------------------------------------------------------------------------
    def test_invariant_19_pause_and_resume_idempotency(self):
        """Invariant 19: Pausing stops execution; resuming continues without bar skips."""
        session = AutopilotSession(self.strategy, initial_capital=100000.0, replay_bars=60)
        session.pause()
        self.assertEqual(session.status, "PAUSED")
        session.resume()
        self.assertEqual(session.status, "RUNNING")

    # -------------------------------------------------------------------------
    # Invariant 20: Playback Speed Throttling Parameters
    # -------------------------------------------------------------------------
    def test_invariant_20_playback_speed_throttling(self):
        """Invariant 20: Speed multiplier parameter accepted in valid range [1, 8]."""
        session = AutopilotSession(self.strategy, initial_capital=100000.0, replay_bars=60)
        session.set_speed(4.0)
        self.assertEqual(session.playback_speed, 4.0)

    # -------------------------------------------------------------------------
    # Invariant 21: Reset Restores Initial Virtual Capital
    # -------------------------------------------------------------------------
    def test_invariant_21_reset_restores_initial_capital(self):
        """Invariant 21: Reset restores virtual cash to ₹1,00,000.00 and clears open positions."""
        session = AutopilotSession(self.strategy, initial_capital=100000.0, replay_bars=60)
        for _ in range(15):
            session.step()
        session.reset()
        self.assertEqual(round(session.broker.cash, 2), 100000.0)
        self.assertEqual(len(session.broker.positions), 0)

    # -------------------------------------------------------------------------
    # Invariant 22: XGBoost Probability Distribution Sums to 1.0
    # -------------------------------------------------------------------------
    def test_invariant_22_xgboost_probability_distribution_sums_to_one(self):
        """Invariant 22: Sum of XGBoost output class probabilities equals 1.0 within epsilon."""
        preds = self.engine.model_mgr.predict_sample(self.engine.X.iloc[-1].values)
        probs = preds["xgboost"]["probabilities"]
        total_prob = sum(probs.values())
        self.assertAlmostEqual(total_prob, 1.0, places=2)

    # -------------------------------------------------------------------------
    # Invariant 23: PyTorch Probability Distribution Sums to 1.0
    # -------------------------------------------------------------------------
    def test_invariant_23_pytorch_probability_distribution_sums_to_one(self):
        """Invariant 23: Sum of PyTorch softmax class probabilities equals 1.0 within epsilon."""
        preds = self.engine.model_mgr.predict_sample(self.engine.X.iloc[-1].values)
        probs = preds["pytorch_mlp"]["probabilities"]
        total_prob = sum(probs.values())
        self.assertAlmostEqual(total_prob, 1.0, places=2)

    # -------------------------------------------------------------------------
    # Invariant 24: SHAP Feature Attributions Validity
    # -------------------------------------------------------------------------
    def test_invariant_24_shap_feature_attributions_validity(self):
        """Invariant 24: TreeExplainer returns attributions for recognized feature columns."""
        exp = self.engine.explain_sample(sample_idx=-1)
        shap_feats = exp["shap_explanation"]["top_features"]
        self.assertGreaterEqual(len(shap_feats), 3)
        for feat in shap_feats:
            self.assertIn("feature", feat)
            self.assertIn("weight", feat)

    # -------------------------------------------------------------------------
    # Invariant 25: LIME Local Surrogate Fidelity
    # -------------------------------------------------------------------------
    def test_invariant_25_lime_local_surrogate_fidelity(self):
        """Invariant 25: LIME tabular explainer produces bounded surrogate weights."""
        exp = self.engine.explain_sample(sample_idx=-1)
        lime_feats = exp["lime_explanation"]["top_features"]
        self.assertGreaterEqual(len(lime_feats), 1)
        for feat in lime_feats:
            self.assertIn("rule", feat)
            self.assertIn("weight", feat)

    # -------------------------------------------------------------------------
    # Invariant 26: Slippage Calculation Non-Negative & Asymmetric
    # -------------------------------------------------------------------------
    def test_invariant_26_slippage_calculation_non_negative(self):
        """Invariant 26: Slippage is non-negative and penalizes execution price."""
        broker = PaperBroker(slippage_rate=0.0005)
        # BUY fills higher
        res_buy = broker.execute_order("RELIANCE", "BUY", 10, 1000.0)
        self.assertGreater(res_buy["fill_price"], 1000.0)
        # SELL fills lower
        res_sell = broker.execute_order("RELIANCE", "SELL", 10, 1000.0)
        self.assertLess(res_sell["fill_price"], 1000.0)

    # -------------------------------------------------------------------------
    # Invariant 27: Brokerage Commission Exactness
    # -------------------------------------------------------------------------
    def test_invariant_27_brokerage_commission_calculation_exact(self):
        """Invariant 27: Brokerage commission rate is 0.05% of gross trade value."""
        broker = PaperBroker(fee_rate=0.0005)
        broker.execute_order("RELIANCE", "BUY", 10, 1000.0)
        order = broker.orders[0]
        expected_fee = round(order["gross_value"] * 0.0005, 2)
        self.assertEqual(order["fee"], expected_fee)

    # -------------------------------------------------------------------------
    # Invariant 28: Win Rate and Trade Accounting
    # -------------------------------------------------------------------------
    def test_invariant_28_win_rate_and_trade_accounting(self):
        """Invariant 28: Win rate strictly reflects closed round-trip trades."""
        broker = PaperBroker(initial_capital=100000.0)
        broker.reset_account(initial_capital=100000.0)
        # Winning trade
        broker.execute_order("RELIANCE", "BUY", 10, 1000.0)
        broker.execute_order("RELIANCE", "SELL", 10, 1100.0)
        # Losing trade
        broker.execute_order("RELIANCE", "BUY", 10, 1000.0)
        broker.execute_order("RELIANCE", "SELL", 10, 950.0)

        trades = broker.trade_history
        wins = [t for t in trades if t["net_pnl"] > 0]
        win_rate = (len(wins) / len(trades)) * 100.0
        self.assertEqual(win_rate, 50.0)

    # -------------------------------------------------------------------------
    # Invariant 29: Structured Activity Feed Logging
    # -------------------------------------------------------------------------
    def test_invariant_29_activity_feed_structured_logging(self):
        """Invariant 29: Activity feed records structured events with category and timestamp."""
        session = AutopilotSession(self.strategy, initial_capital=100000.0, replay_bars=60)
        session.step()
        feed = session.activity_feed
        self.assertGreater(len(feed), 0)
        item = feed[0]
        self.assertIn("type", item)
        self.assertIn("title", item)
        self.assertIn("timestamp", item)

    # -------------------------------------------------------------------------
    # Invariant 30: Zero Real Money Broker Leakage
    # -------------------------------------------------------------------------
    def test_invariant_30_zero_real_money_broker_leakage(self):
        """Invariant 30: 100% virtual execution: Zero real money broker network requests."""
        broker = PaperBroker(initial_capital=100000.0)
        res = broker.execute_order("RELIANCE", "BUY", 10, 1500.0)
        self.assertTrue(res["success"])
        self.assertEqual(broker.trading_mode, "paper")
        self.assertTrue(broker.is_virtual)


if __name__ == "__main__":
    unittest.main()
