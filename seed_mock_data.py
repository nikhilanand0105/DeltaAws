import datetime
import random
from app import app, db
from models import Account, Strategy, StrategyState, TradeLog, LocalSignalLog, GlobalSetting

def seed():
    with app.app_context():
        print("Starting Database Seeding for DBMS Project...")

        # 1. Ensure Global Settings
        dry_run_setting = GlobalSetting.query.filter_by(key="local_bot_dry_run").first()
        if not dry_run_setting:
            db.session.add(GlobalSetting(key="local_bot_dry_run", value="true"))
        else:
            dry_run_setting.value = "true" # Keep dry run on so no real money is used

        passphrase_s = GlobalSetting.query.filter_by(key="passphrase").first()
        if not passphrase_s:
            db.session.add(GlobalSetting(key="passphrase", value="my_secure_trading_passphrase_123"))

        # 2. Seed Accounts
        accounts_spec = [
            {
                "name": "Alpha Momentum Fund (Paper)",
                "api_key": "MOCK_ALPHA_KEY_9847192847",
                "api_secret": "MOCK_ALPHA_SECRET_1928374619",
                "leverage": 50,
                "balance_buffer_pct": 80.0,
                "sizing_type": "percentage",
                "fixed_amount": 10.0,
                "is_active": True,
                "local_strategy_enabled": True
            },
            {
                "name": "Delta Grid & Arbitrage (Paper)",
                "api_key": "MOCK_GRID_KEY_3847291847",
                "api_secret": "MOCK_GRID_SECRET_9283746192",
                "leverage": 20,
                "balance_buffer_pct": 60.0,
                "sizing_type": "percentage",
                "fixed_amount": 10.0,
                "is_active": True,
                "local_strategy_enabled": True
            },
            {
                "name": "Institutional Swing Pool (Paper)",
                "api_key": "MOCK_SWING_KEY_1928374650",
                "api_secret": "MOCK_SWING_SECRET_8374619283",
                "leverage": 10,
                "balance_buffer_pct": 50.0,
                "sizing_type": "fixed",
                "fixed_amount": 50.0,
                "is_active": True,
                "local_strategy_enabled": True
            },
            {
                "name": "Retail Algorithmic Vault (Paper)",
                "api_key": "MOCK_RETAIL_KEY_8472918374",
                "api_secret": "MOCK_RETAIL_SECRET_3746192837",
                "leverage": 25,
                "balance_buffer_pct": 70.0,
                "sizing_type": "percentage",
                "fixed_amount": 10.0,
                "is_active": True,
                "local_strategy_enabled": True
            }
        ]

        created_accounts = []
        for a_spec in accounts_spec:
            acc = Account.query.filter_by(name=a_spec["name"]).first()
            if not acc:
                acc = Account(**a_spec)
                db.session.add(acc)
                db.session.flush()
            else:
                for k, v in a_spec.items():
                    setattr(acc, k, v)
            created_accounts.append(acc)

        db.session.commit()
        print(f"Created/Verified {len(created_accounts)} accounts.")

        # 3. Seed Strategies
        strategies_spec = [
            {"account_id": created_accounts[0].id, "name": "Chandelier Trend Follower", "sizing_type": "percentage", "balance_buffer_pct": 30.0, "fixed_amount": 10.0, "leverage": 50},
            {"account_id": created_accounts[0].id, "name": "ZLSMA Momentum Scalper", "sizing_type": "percentage", "balance_buffer_pct": 20.0, "fixed_amount": 10.0, "leverage": 50},
            {"account_id": created_accounts[1].id, "name": "Statistical Arbitrage Grid", "sizing_type": "percentage", "balance_buffer_pct": 40.0, "fixed_amount": 10.0, "leverage": 20},
            {"account_id": created_accounts[2].id, "name": "Macro Trend Breakout", "sizing_type": "fixed", "balance_buffer_pct": 50.0, "fixed_amount": 50.0, "leverage": 10},
            {"account_id": created_accounts[3].id, "name": "Volatility Breakout", "sizing_type": "percentage", "balance_buffer_pct": 35.0, "fixed_amount": 10.0, "leverage": 25},
        ]

        created_strategies = []
        for s_spec in strategies_spec:
            strat = Strategy.query.filter_by(account_id=s_spec["account_id"], name=s_spec["name"]).first()
            if not strat:
                strat = Strategy(**s_spec)
                db.session.add(strat)
                db.session.flush()
            created_strategies.append(strat)

        db.session.commit()
        print(f"Created/Verified {len(created_strategies)} strategies.")

        # 4. Seed Live Active Strategy Positions in StrategyState
        # Real approximate mark prices: ETH ~2423, BTC ~81450, SOL ~103.8
        now = datetime.datetime.now(datetime.timezone.utc)
        positions_spec = [
            {
                "account_id": created_accounts[0].id,
                "strategy_id": created_strategies[0].id,
                "symbol": "ETHUSD",
                "position_size": 25.0, # Long 25 lots
                "entry_price": 2415.50,
                "sl_dist": 35.50,
                "tp1_price": 2468.75,
                "tp2_price": 2522.00,
                "tp1_hit": False,
                "tp2_hit": False,
                "current_sl": 2380.00,
                "last_signal_time": int(now.timestamp())
            },
            {
                "account_id": created_accounts[1].id,
                "strategy_id": created_strategies[2].id,
                "symbol": "BTCUSD",
                "position_size": -15.0, # Short 15 lots
                "entry_price": 81680.00,
                "sl_dist": 820.00,
                "tp1_price": 80450.00,
                "tp2_price": 79220.00,
                "tp1_hit": False,
                "tp2_hit": False,
                "current_sl": 82500.00,
                "last_signal_time": int(now.timestamp())
            },
            {
                "account_id": created_accounts[2].id,
                "strategy_id": created_strategies[3].id,
                "symbol": "SOLUSD",
                "position_size": 40.0, # Long 40 lots
                "entry_price": 101.40,
                "sl_dist": 3.40,
                "tp1_price": 106.50,
                "tp2_price": 111.60,
                "tp1_hit": False,
                "tp2_hit": False,
                "current_sl": 98.00,
                "last_signal_time": int(now.timestamp())
            },
            {
                "account_id": created_accounts[3].id,
                "strategy_id": created_strategies[4].id,
                "symbol": "ETHUSD",
                "position_size": -12.0, # Short 12 lots
                "entry_price": 2432.80,
                "sl_dist": 28.00,
                "tp1_price": 2390.80,
                "tp2_price": 2348.80,
                "tp1_hit": False,
                "tp2_hit": False,
                "current_sl": 2460.80,
                "last_signal_time": int(now.timestamp())
            }
        ]

        for p_spec in positions_spec:
            state = StrategyState.query.filter_by(account_id=p_spec["account_id"], symbol=p_spec["symbol"]).first()
            if not state:
                state = StrategyState(**p_spec)
                db.session.add(state)
            else:
                for k, v in p_spec.items():
                    setattr(state, k, v)

        db.session.commit()
        print(f"Created/Verified {len(positions_spec)} active strategy states.")

        # 5. Seed Historical Trade Logs
        # Only seed if fewer than 10 logs exist
        if TradeLog.query.count() < 10:
            mock_trades = [
                # ETH Trades
                {"ticker": "ETHUSD", "action": "buy", "source": "local_strategy", "status": "success", "details": "Local Strategy Long Entry: 25 lots @ 2380.20", "delta_h": 96, "pnl": None},
                {"ticker": "ETHUSD", "action": "close_long", "source": "local_strategy", "status": "success", "details": "Local Strategy Long Exit: 25 lots @ 2425.40 - PnL: +113.00 USD (Fees: 0.60 USD)", "delta_h": 90, "pnl": 113.00},
                {"ticker": "ETHUSD", "action": "sell", "source": "local_strategy", "status": "success", "details": "Local Strategy Short Entry: 20 lots @ 2440.00", "delta_h": 82, "pnl": None},
                {"ticker": "ETHUSD", "action": "close_short", "source": "local_strategy", "status": "success", "details": "Local Strategy Short Exit: 20 lots @ 2410.50 - PnL: +59.00 USD (Fees: 0.48 USD)", "delta_h": 76, "pnl": 59.00},
                {"ticker": "ETHUSD", "action": "buy", "source": "local_strategy", "status": "success", "details": "Local Strategy Long Entry: 15 lots @ 2415.00", "delta_h": 68, "pnl": None},
                {"ticker": "ETHUSD", "action": "close_long", "source": "local_strategy", "status": "success", "details": "Local Strategy Long Exit: 15 lots @ 2392.00 - PnL: -34.50 USD (Fees: 0.36 USD)", "delta_h": 64, "pnl": -34.50},
                {"ticker": "ETHUSD", "action": "buy", "source": "local_strategy", "status": "success", "details": "Local Strategy Long Entry: 30 lots @ 2398.00", "delta_h": 50, "pnl": None},
                {"ticker": "ETHUSD", "action": "close_long", "source": "local_strategy", "status": "success", "details": "Local Strategy Long Exit: 30 lots @ 2442.10 - PnL: +132.30 USD (Fees: 0.72 USD)", "delta_h": 44, "pnl": 132.30},

                # BTC Trades
                {"ticker": "BTCUSD", "action": "sell", "source": "local_strategy", "status": "success", "details": "Local Strategy Short Entry: 10 lots @ 82400.00", "delta_h": 92, "pnl": None},
                {"ticker": "BTCUSD", "action": "close_short", "source": "local_strategy", "status": "success", "details": "Local Strategy Short Exit: 10 lots @ 81100.00 - PnL: +130.00 USD (Fees: 0.82 USD)", "delta_h": 85, "pnl": 130.00},
                {"ticker": "BTCUSD", "action": "buy", "source": "local_strategy", "status": "success", "details": "Local Strategy Long Entry: 12 lots @ 80950.00", "delta_h": 72, "pnl": None},
                {"ticker": "BTCUSD", "action": "close_long", "source": "local_strategy", "status": "success", "details": "Local Strategy Long Exit: 12 lots @ 81920.00 - PnL: +116.40 USD (Fees: 0.98 USD)", "delta_h": 66, "pnl": 116.40},
                {"ticker": "BTCUSD", "action": "sell", "source": "local_strategy", "status": "success", "details": "Local Strategy Short Entry: 8 lots @ 81800.00", "delta_h": 40, "pnl": None},
                {"ticker": "BTCUSD", "action": "close_short", "source": "local_strategy", "status": "success", "details": "Local Strategy Short Exit: 8 lots @ 82250.00 - PnL: -36.00 USD (Fees: 0.65 USD)", "delta_h": 36, "pnl": -36.00},
                {"ticker": "BTCUSD", "action": "buy", "source": "local_strategy", "status": "success", "details": "Local Strategy Long Entry: 15 lots @ 81200.00", "delta_h": 28, "pnl": None},
                {"ticker": "BTCUSD", "action": "close_long", "source": "local_strategy", "status": "success", "details": "Local Strategy Long Exit: 15 lots @ 81750.00 - PnL: +82.50 USD (Fees: 1.22 USD)", "delta_h": 22, "pnl": 82.50},

                # SOL Trades
                {"ticker": "SOLUSD", "action": "buy", "source": "local_strategy", "status": "success", "details": "Local Strategy Long Entry: 40 lots @ 98.50", "delta_h": 80, "pnl": None},
                {"ticker": "SOLUSD", "action": "close_long", "source": "local_strategy", "status": "success", "details": "Local Strategy Long Exit: 40 lots @ 103.20 - PnL: +188.00 USD (Fees: 0.40 USD)", "delta_h": 74, "pnl": 188.00},
                {"ticker": "SOLUSD", "action": "sell", "source": "local_strategy", "status": "success", "details": "Local Strategy Short Entry: 35 lots @ 104.80", "delta_h": 58, "pnl": None},
                {"ticker": "SOLUSD", "action": "close_short", "source": "local_strategy", "status": "success", "details": "Local Strategy Short Exit: 35 lots @ 101.90 - PnL: +101.50 USD (Fees: 0.36 USD)", "delta_h": 52, "pnl": 101.50},
                {"ticker": "SOLUSD", "action": "buy", "source": "local_strategy", "status": "success", "details": "Local Strategy Long Entry: 50 lots @ 102.10", "delta_h": 32, "pnl": None},
                {"ticker": "SOLUSD", "action": "close_long", "source": "local_strategy", "status": "success", "details": "Local Strategy Long Exit: 50 lots @ 100.80 - PnL: -65.00 USD (Fees: 0.51 USD)", "delta_h": 26, "pnl": -65.00},
                {"ticker": "SOLUSD", "action": "buy", "source": "local_strategy", "status": "success", "details": "Local Strategy Long Entry: 45 lots @ 101.50", "delta_h": 16, "pnl": None},
                {"ticker": "SOLUSD", "action": "close_long", "source": "local_strategy", "status": "success", "details": "Local Strategy Long Exit: 45 lots @ 104.20 - PnL: +121.50 USD (Fees: 0.46 USD)", "delta_h": 10, "pnl": 121.50},
            ]

            base_time = now
            for trade in mock_trades:
                trade_time = base_time - datetime.timedelta(hours=trade["delta_h"], minutes=random.randint(2, 45))
                log_entry = TradeLog(
                    timestamp=trade_time,
                    ticker=trade["ticker"],
                    action=trade["action"],
                    source=trade["source"],
                    status=trade["status"],
                    details=trade["details"]
                )
                db.session.add(log_entry)

            db.session.commit()
            print(f"Created {len(mock_trades)} historical trade logs.")

        # 6. Seed Local Signal Logs
        if LocalSignalLog.query.count() < 10:
            mock_signals = [
                {"account_id": created_accounts[0].id, "account_name": created_accounts[0].name, "signal_type": "BUY", "price": 2415.50, "quantity": 25.0, "stop_loss": 2380.00, "take_profit_1": 2468.75, "take_profit_2": 2522.00, "is_matched": True, "delta_h": 3},
                {"account_id": created_accounts[1].id, "account_name": created_accounts[1].name, "signal_type": "SELL", "price": 81680.00, "quantity": 15.0, "stop_loss": 82500.00, "take_profit_1": 80450.00, "take_profit_2": 79220.00, "is_matched": True, "delta_h": 4},
                {"account_id": created_accounts[2].id, "account_name": created_accounts[2].name, "signal_type": "BUY", "price": 101.40, "quantity": 40.0, "stop_loss": 98.00, "take_profit_1": 106.50, "take_profit_2": 111.60, "is_matched": True, "delta_h": 5},
                {"account_id": created_accounts[3].id, "account_name": created_accounts[3].name, "signal_type": "SELL", "price": 2432.80, "quantity": 12.0, "stop_loss": 2460.80, "take_profit_1": 2390.80, "take_profit_2": 2348.80, "is_matched": True, "delta_h": 6},
                {"account_id": created_accounts[0].id, "account_name": created_accounts[0].name, "signal_type": "TP1", "price": 2465.00, "quantity": 12.5, "stop_loss": 2415.50, "take_profit_1": 2465.00, "take_profit_2": 2510.00, "is_matched": True, "delta_h": 12},
                {"account_id": created_accounts[1].id, "account_name": created_accounts[1].name, "signal_type": "EXIT_ZLSMA", "price": 81920.00, "quantity": 12.0, "stop_loss": 80950.00, "take_profit_1": 82500.00, "take_profit_2": 83200.00, "is_matched": True, "delta_h": 18},
                {"account_id": created_accounts[2].id, "account_name": created_accounts[2].name, "signal_type": "TP2", "price": 105.80, "quantity": 20.0, "stop_loss": 101.40, "take_profit_1": 103.50, "take_profit_2": 105.80, "is_matched": True, "delta_h": 24},
                {"account_id": created_accounts[0].id, "account_name": created_accounts[0].name, "signal_type": "BUY", "price": 2398.00, "quantity": 30.0, "stop_loss": 2360.00, "take_profit_1": 2440.00, "take_profit_2": 2480.00, "is_matched": True, "delta_h": 44},
                {"account_id": created_accounts[1].id, "account_name": created_accounts[1].name, "signal_type": "SELL", "price": 82400.00, "quantity": 10.0, "stop_loss": 83100.00, "take_profit_1": 81200.00, "take_profit_2": 80100.00, "is_matched": True, "delta_h": 85},
            ]

            for sig in mock_signals:
                sig_time = now - datetime.timedelta(hours=sig["delta_h"])
                sig_entry = LocalSignalLog(
                    timestamp=sig_time,
                    account_id=sig["account_id"],
                    account_name=sig["account_name"],
                    signal_type=sig["signal_type"],
                    price=sig["price"],
                    quantity=sig["quantity"],
                    stop_loss=sig["stop_loss"],
                    take_profit_1=sig["take_profit_1"],
                    take_profit_2=sig["take_profit_2"],
                    is_matched=sig["is_matched"]
                )
                db.session.add(sig_entry)

            db.session.commit()
            print(f"Created {len(mock_signals)} local signal logs.")

        print("Database Seeding Completed Successfully!")

if __name__ == "__main__":
    seed()
