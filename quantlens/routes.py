"""
QuantLens-XAI Flask Blueprint.
Provides REST API endpoints and web UI routing for:
1. Natural language strategy parsing with local Ollama LLM.
2. Strategy schema validation and rule verification.
3. Real historical backtesting with financial KPIs and candlestick series.
4. XAI explainability (real SHAP, LIME, and Slide 9 empirical evaluation metrics).
5. QuantLens Paper Broker (Groww-inspired virtual trading, historical simulation replay, order ledger, audit log).
"""

import os
import json
import time
import logging
from typing import Dict, Any
from flask import Blueprint, request, jsonify, render_template

from quantlens.strategy_schema import StrategyDefinition, StrategyParseResponse
from quantlens.strategy_validator import validate_strategy
from quantlens.llm_parser import parse_strategy_with_llm
from quantlens.backtest_engine import run_strategy_backtest
from quantlens.xai_engine import get_xai_explanation
from quantlens.xai_evaluation import evaluate_xai_metrics
from quantlens.paper_broker import get_paper_broker
from quantlens.simulation_engine import SimulationEngine
from quantlens.data_loader import get_available_symbols, load_historical_ohlcv

logger = logging.getLogger(__name__)

quantlens_bp = Blueprint("quantlens", __name__, template_folder="../templates")


@quantlens_bp.route("/quantlens")
def quantlens_home():
    """Renders the main QuantLens-XAI unified platform."""
    broker = get_paper_broker()
    summary = broker.get_dashboard_summary()
    return render_template("quantlens.html", broker_summary=summary)


@quantlens_bp.route("/api/quantlens/symbols", methods=["GET"])
def api_symbols():
    """Returns available historical symbols."""
    symbols = get_available_symbols()
    return jsonify({"success": True, "symbols": symbols})


@quantlens_bp.route("/api/quantlens/parse-strategy", methods=["POST"])
def api_parse_strategy():
    """Parses a natural language trading strategy prompt using local Ollama LLM."""
    data = request.get_json(silent=True) or {}
    prompt = data.get("prompt", "").strip()
    preferred_symbol = data.get("symbol", "RELIANCE")

    if not prompt:
        return jsonify({"success": False, "error": "Prompt cannot be empty"}), 400

    try:
        response_model: StrategyParseResponse = parse_strategy_with_llm(
            prompt=prompt,
            preferred_symbol=preferred_symbol
        )
        return jsonify({
            "success": True,
            "data": response_model.model_dump()
        })
    except Exception as e:
        logger.exception("Error parsing strategy with Ollama")
        return jsonify({"success": False, "error": str(e)}), 500


@quantlens_bp.route("/api/quantlens/validate-strategy", methods=["POST"])
def api_validate_strategy():
    """Validates a structured strategy JSON payload against Pydantic schema and financial logic rules."""
    data = request.get_json(silent=True) or {}
    try:
        strat = StrategyDefinition(**data)
        is_valid, errors = validate_strategy(strat)
        return jsonify({
            "success": True,
            "valid": is_valid,
            "errors": errors,
            "warnings": [],
            "strategy": strat.model_dump()
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "valid": False,
            "errors": [str(e)],
            "warnings": []
        }), 200


@quantlens_bp.route("/api/quantlens/backtest", methods=["POST"])
def api_backtest():
    """Runs event-driven backtesting on historical data for the parsed strategy."""
    data = request.get_json(silent=True) or {}
    try:
        # If wrapped in strategy key
        strat_dict = data.get("strategy", data)
        if "strategy_id" not in strat_dict:
            strat_dict["strategy_id"] = f"strat-{int(time.time())}"
        if "raw_prompt" not in strat_dict:
            strat_dict["raw_prompt"] = "Manual Backtest"

        strategy = StrategyDefinition(**strat_dict)
        start_date = data.get("start_date")
        end_date = data.get("end_date")
        
        result = run_strategy_backtest(strategy, start_date=start_date, end_date=end_date)
        return jsonify({
            "success": True,
            "result": result
        })
    except Exception as e:
        logger.exception("Error running backtest")
        return jsonify({"success": False, "error": str(e)}), 500


@quantlens_bp.route("/api/quantlens/xai-explain", methods=["GET", "POST"])
def api_xai_explain():
    """Computes real SHAP, LIME, and Slide 9 empirical evaluation metrics."""
    data = request.get_json(silent=True) or {} if request.method == "POST" else request.args
    symbol = data.get("symbol", "RELIANCE")
    bar_index = int(data.get("bar_index", -1))

    try:
        explanation = get_xai_explanation(symbol=symbol, bar_index=bar_index)
        eval_metrics = evaluate_xai_metrics(symbol=symbol, use_cache=True)

        return jsonify({
            "success": True,
            "explanation": explanation,
            "evaluation_metrics": eval_metrics
        })
    except Exception as e:
        logger.exception("Error generating XAI explanation")
        return jsonify({"success": False, "error": str(e)}), 500


@quantlens_bp.route("/api/quantlens/paper-broker/dashboard", methods=["GET"])
def api_broker_dashboard():
    """Returns current paper broker account state, holdings, orders, and audit log."""
    broker = get_paper_broker()
    # Update latest mark to market price for open positions
    for sym in broker.positions.keys():
        try:
            df = load_historical_ohlcv(sym)
            if not df.empty:
                last_px = float(df["close"].iloc[-1])
                broker.update_market_prices({sym: last_px})
        except Exception:
            pass

    return jsonify({
        "success": True,
        "dashboard": broker.get_dashboard_summary()
    })


@quantlens_bp.route("/api/quantlens/paper-broker/order", methods=["POST"])
def api_broker_order():
    """Executes a virtual paper order in the QuantLens Paper Broker."""
    data = request.get_json(silent=True) or {}
    symbol = data.get("symbol", "RELIANCE")
    side = data.get("side", "BUY").upper()
    quantity = int(data.get("quantity", 1))
    price = float(data.get("price", 0.0))
    rule_reason = data.get("rule_reason", "Manual Paper Trade")
    strategy_id = data.get("strategy_id", "MANUAL")

    broker = get_paper_broker()

    # If price is 0, fetch latest close
    if price <= 0:
        try:
            df = load_historical_ohlcv(symbol)
            price = float(df["close"].iloc[-1])
        except Exception:
            price = 1000.0

    result = broker.execute_order(
        symbol=symbol,
        side=side,
        quantity=quantity,
        price=price,
        order_type="market",
        strategy_id=strategy_id,
        rule_reason=rule_reason
    )

    return jsonify({
        "success": result.get("success", False),
        "result": result,
        "dashboard": broker.get_dashboard_summary()
    })


@quantlens_bp.route("/api/quantlens/paper-broker/replay", methods=["POST"])
def api_broker_replay():
    """Runs historical simulation replay against the Paper Broker."""
    data = request.get_json(silent=True) or {}
    strat_dict = data.get("strategy", {})
    if not strat_dict:
        strat_dict = {
            "strategy_id": "sim-default-1",
            "raw_prompt": "Replay Simulation",
            "symbol": data.get("symbol", "RELIANCE")
        }
    if "strategy_id" not in strat_dict:
        strat_dict["strategy_id"] = f"strat-{int(time.time())}"
    if "raw_prompt" not in strat_dict:
        strat_dict["raw_prompt"] = "Replay Simulation"

    window_bars = int(data.get("window_bars", 60))
    reset_first = bool(data.get("reset_broker", False))
    ml_filter = bool(data.get("ml_filter", False))

    try:
        strategy = StrategyDefinition(**strat_dict)
        sim = SimulationEngine()
        result = sim.run_replay(
            strategy=strategy,
            window_bars=window_bars,
            reset_broker_first=reset_first,
            ml_filter=ml_filter
        )
        return jsonify({
            "success": True,
            "replay": result
        })
    except Exception as e:
        logger.exception("Error executing simulation replay")
        return jsonify({"success": False, "error": str(e)}), 500


@quantlens_bp.route("/api/quantlens/paper-broker/reset", methods=["POST"])
def api_broker_reset():
    """Resets paper broker virtual funds to ₹1,00,000."""
    data = request.get_json(silent=True) or {}
    initial_cash = float(data.get("initial_capital", 100000.0))
    broker = get_paper_broker()
    broker.reset_account(initial_capital=initial_cash)
    return jsonify({
        "success": True,
        "message": f"QuantLens Paper Broker successfully reset to ₹{initial_cash:,.2f} virtual funds.",
        "dashboard": broker.get_dashboard_summary()
    })


@quantlens_bp.route("/api/quantlens/models/status", methods=["GET"])
def api_models_status():
    """Returns local LLM and ML model readiness status."""
    import requests
    ollama_ok = False
    ollama_model = "qwen2.5:0.5b"
    try:
        r = requests.get("http://127.0.0.1:11434/api/tags", timeout=1.0)
        if r.status_code == 200:
            ollama_ok = True
    except Exception:
        ollama_ok = False

    xgb_exists = os.path.exists("models/xgboost_reliance.json")
    torch_exists = os.path.exists("models/pytorch_mlp_reliance.pt")
    meta_path = "models/models_meta_reliance.json"
    meta = {}
    if os.path.exists(meta_path):
        try:
            with open(meta_path, "r") as f:
                meta = json.load(f)
        except Exception:
            pass

    return jsonify({
        "success": True,
        "ollama": {
            "online": ollama_ok,
            "endpoint": "http://127.0.0.1:11434",
            "model": ollama_model,
            "hardware": "Apple M1 Pro (Metal GPU accelerated)"
        },
        "ml_models": {
            "symbol": "RELIANCE",
            "xgboost_available": xgb_exists,
            "pytorch_available": torch_exists,
            "metadata": meta
        }
    })
