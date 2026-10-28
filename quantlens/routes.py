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
from flask import Blueprint, request, jsonify, render_template, Response

from quantlens.strategy_schema import StrategyDefinition, StrategyParseResponse
from quantlens.strategy_validator import validate_strategy
from quantlens.llm_parser import parse_strategy_with_llm
from quantlens.backtest_engine import run_strategy_backtest
from quantlens.xai_engine import get_xai_explanation
from quantlens.xai_evaluation import evaluate_xai_metrics
from quantlens.paper_broker import get_paper_broker
from quantlens.simulation_engine import SimulationEngine
from quantlens.data_loader import get_available_symbols, load_historical_ohlcv
from quantlens.orchestrator import (
    create_analysis_run,
    get_analysis_run,
    execute_analysis_pipeline_generator,
    answer_advisor_question
)
from quantlens.autopilot_engine import (
    AutopilotSession,
    init_autopilot_session,
    get_autopilot_session,
    _AUTOPILOT_SESSIONS
)

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


@quantlens_bp.route("/api/quantlens/analyze-and-run", methods=["POST"])
def api_analyze_and_run():
    """Initializes an orchestrated 8-stage Strategy Intelligence analysis run."""
    data = request.get_json(silent=True) or {}
    prompt = data.get("prompt", "").strip()
    symbol = data.get("symbol", "RELIANCE")

    if not prompt:
        return jsonify({"success": False, "error": "Prompt cannot be empty"}), 400

    run_id = create_analysis_run(prompt=prompt, symbol=symbol)
    return jsonify({
        "success": True,
        "run_id": run_id,
        "symbol": symbol,
        "stream_url": f"/api/quantlens/analysis-stream/{run_id}"
    })


@quantlens_bp.route("/api/quantlens/analysis-stream/<run_id>", methods=["GET"])
def api_analysis_stream(run_id: str):
    """Server-Sent Events (SSE) streaming endpoint for Strategy Intelligence Mission Control."""
    return Response(
        execute_analysis_pipeline_generator(run_id),
        mimetype="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "X-Accel-Buffering": "no",
            "Connection": "keep-alive",
            "Access-Control-Allow-Origin": "*"
        }
    )


@quantlens_bp.route("/api/quantlens/analysis-status/<run_id>", methods=["GET"])
def api_analysis_status(run_id: str):
    """Returns current status and complete payload for an analysis run."""
    run_info = get_analysis_run(run_id)
    if not run_info:
        return jsonify({"success": False, "error": "Run not found"}), 404
    return jsonify({"success": True, "data": run_info})


@quantlens_bp.route("/api/quantlens/advisor/qa", methods=["POST"])
def api_advisor_qa():
    """Grounded contextual Q&A endpoint for the AI Strategy Advisor."""
    data = request.get_json(silent=True) or {}
    question = data.get("question", "").strip()
    strategy_dict = data.get("strategy", {})

    if not question:
        return jsonify({"success": False, "error": "Question cannot be empty"}), 400

    result = answer_advisor_question(question=question, strategy_dict=strategy_dict)
    return jsonify(result)


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


@quantlens_bp.route("/api/quantlens/db-status", methods=["GET"])
def api_db_status():
    """Returns real-time health and record metrics for both SQLite and MongoDB."""
    from quantlens.db_mongodb import get_mongodb
    import sqlite3

    # 1. MongoDB Status
    mongo_mgr = get_mongodb()
    mongo_status = mongo_mgr.get_status()

    # 2. SQLite Status
    sqlite_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "instance", "local.db")
    sqlite_status = {"connected": False, "tables": {}}
    if os.path.exists(sqlite_path):
        try:
            conn = sqlite3.connect(sqlite_path)
            cur = conn.cursor()
            cur.execute("PRAGMA integrity_check;")
            integrity = cur.fetchone()[0]
            table_counts = {}
            for t in ["accounts", "settings", "strategies", "strategy_states", "trade_logs", "local_signal_logs"]:
                try:
                    cur.execute(f"SELECT COUNT(*) FROM {t}")
                    table_counts[t] = cur.fetchone()[0]
                except Exception:
                    pass
            conn.close()
            sqlite_status = {
                "connected": True,
                "file_path": sqlite_path,
                "integrity": integrity,
                "engine": "SQLite 3 (via SQLAlchemy 2.0)",
                "tables": table_counts
            }
        except Exception as e:
            sqlite_status = {"connected": False, "error": str(e)}

    return jsonify({
        "success": True,
        "architecture": "Hybrid SQL (SQLite) + NoSQL (MongoDB)",
        "sqlite": sqlite_status,
        "mongodb": mongo_status
    })


# -------------------------------------------------------------
# QuantLens Autopilot Endpoints
# -------------------------------------------------------------

@quantlens_bp.route("/api/quantlens/autopilot/init", methods=["POST"])
def api_autopilot_init():
    """Initializes a new continuous paper-trading Autopilot session."""
    data = request.get_json() or {}
    symbol = data.get("symbol", "RELIANCE").upper().replace(".NS", "")
    scenario = data.get("scenario", "trend_following")
    window_bars = int(data.get("window_bars", 120))
    initial_capital = float(data.get("initial_capital", 100000.0))
    synthetic_type = data.get("synthetic_type")

    raw_strat = data.get("strategy")
    if isinstance(raw_strat, dict) and "strategy_id" in raw_strat:
        try:
            strategy = StrategyDefinition(**raw_strat)
        except Exception:
            strategy = StrategyDefinition(
                strategy_id=raw_strat.get("strategy_id", f"ap-strat-{int(time.time())}"),
                strategy_name=raw_strat.get("strategy_name", "EMA Crossover + RSI Strategy"),
                symbol=symbol,
                raw_prompt=raw_strat.get("raw_prompt", "Autopilot continuous trading")
            )
    else:
        strategy = StrategyDefinition(
            strategy_id=f"ap-strat-{int(time.time())}",
            strategy_name=f"{symbol} EMA Crossover + RSI Autopilot",
            symbol=symbol,
            raw_prompt=f"Buy {symbol} whenever EMA 10 crosses above EMA 30 and RSI 14 is below 65. Sell when EMA 10 crosses below EMA 30 or SL 2% / TP 4%."
        )

    session = init_autopilot_session(
        strategy=strategy,
        symbol=symbol,
        scenario=scenario,
        window_bars=window_bars,
        initial_capital=initial_capital,
        synthetic_type=synthetic_type
    )

    return jsonify({"success": True, **session.get_state()})


@quantlens_bp.route("/api/quantlens/autopilot/step", methods=["POST"])
def api_autopilot_step():
    """Advances simulation forward by N steps causally."""
    data = request.get_json() or {}
    session_id = data.get("session_id", "")
    steps = max(1, min(int(data.get("steps", 1)), 50))

    session = get_autopilot_session(session_id)
    if not session:
        return jsonify({"success": False, "error": f"Session '{session_id}' not found."}), 404

    for _ in range(steps):
        session.step()
        if session.status == "COMPLETED" and not session.loop_mode:
            break

    return jsonify({"success": True, **session.get_state()})


@quantlens_bp.route("/api/quantlens/autopilot/control", methods=["POST"])
def api_autopilot_control():
    """Controls simulation execution state: play, pause, resume, restart, set_speed, skip_to_signal, set_loop."""
    data = request.get_json() or {}
    session_id = data.get("session_id", "")
    action = data.get("action", "").lower()

    session = get_autopilot_session(session_id)
    if not session:
        return jsonify({"success": False, "error": f"Session '{session_id}' not found."}), 404

    if action in ("play", "resume"):
        session.status = "RUNNING"
        session._record_activity(
            event_type="SYSTEM",
            title="Autopilot Simulation Resumed",
            detail=f"Automated execution active at {session.playback_speed}x speed.",
            status="info"
        )
    elif action == "pause":
        session.status = "PAUSED"
        session._record_activity(
            event_type="SYSTEM",
            title="Autopilot Simulation Paused",
            detail=f"Replay halted at bar {session.current_idx} of {session.total_bars}.",
            status="warning"
        )
    elif action == "restart":
        session.current_idx = 1
        session.broker.reset_account(session.initial_capital)
        session.status = "READY"
        session.equity_curve = [{
            "step": 0,
            "date": str(session.df["date"].iloc[0])[:10] if "date" in session.df.columns else "Day 0",
            "timestamp": str(session.df["date"].iloc[0])[:10] if "date" in session.df.columns else "Day 0",
            "equity": session.initial_capital,
            "cash": session.initial_capital,
            "invested": 0.0,
            "unrealized_pnl": 0.0,
            "realized_pnl": 0.0,
            "drawdown_pct": 0.0
        }]
        session._record_activity(
            event_type="SYSTEM",
            title="Simulation Restarted",
            detail=f"Account reset to ₹{session.initial_capital:,.2f}. Replay returned to day 1.",
            status="info"
        )
    elif action == "set_speed":
        speed = float(data.get("speed", 1))
        session.playback_speed = speed
        session._record_activity(
            event_type="SYSTEM",
            title="Playback Speed Adjusted",
            detail=f"Speed changed to {speed}x.",
            values={"speed": speed},
            status="info"
        )
    elif action == "set_loop":
        loop = bool(data.get("loop", False))
        session.loop_mode = loop
        session._record_activity(
            event_type="SYSTEM",
            title="Demo Loop Mode Changed",
            detail=f"Continuous demo loop mode {'ENABLED' if loop else 'DISABLED'}.",
            values={"loop": loop},
            status="info"
        )
    elif action == "skip_to_signal":
        session.skip_to_next_signal()

    session.persist_session_checkpoint()
    return jsonify({"success": True, **session.get_state()})


@quantlens_bp.route("/api/quantlens/autopilot/state/<session_id>", methods=["GET"])
@quantlens_bp.route("/api/quantlens/autopilot/state", methods=["GET"])
def api_autopilot_state(session_id: str = ""):
    """Returns current state and chart data for the active Autopilot session."""
    session = get_autopilot_session(session_id)
    if not session:
        return jsonify({"success": False, "error": f"Session '{session_id}' not found."}), 404
    return jsonify({"success": True, **session.get_state()})


@quantlens_bp.route("/api/quantlens/autopilot/explain-trade", methods=["GET", "POST"])
def api_autopilot_explain_trade():
    """Returns transparent explainability package (rules, ML, SHAP, LIME, narrative) for a trade."""
    if request.method == "POST":
        data = request.get_json() or {}
        order_id = data.get("order_id", "")
        session_id = data.get("session_id", "")
    else:
        order_id = request.args.get("order_id", "")
        session_id = request.args.get("session_id", "")

    session = get_autopilot_session(session_id)
    if not session:
        return jsonify({"success": False, "error": "No active Autopilot session."}), 404

    explanation = session.get_trade_explanation(order_id)
    return jsonify(explanation)


@quantlens_bp.route("/api/quantlens/autopilot/prepare-demo", methods=["POST"])
def api_autopilot_prepare_demo():
    """Pre-configures a flawless one-click demonstration session with Scenario A (Trend Following)."""
    strategy = StrategyDefinition(
        strategy_id=f"demo-strat-{int(time.time())}",
        strategy_name="EMA Crossover + RSI Momentum Strategy",
        symbol="RELIANCE",
        raw_prompt="Buy RELIANCE whenever EMA 10 crosses above EMA 30 and RSI 14 is below 65. Sell when EMA 10 crosses below EMA 30, or when stop-loss reaches 2% or take-profit reaches 4%. Start with ₹1,00,000 and allocate a maximum of 10% of available cash per position."
    )
    session = init_autopilot_session(
        strategy=strategy,
        symbol="RELIANCE",
        scenario="trend_following",
        window_bars=120,
        initial_capital=100000.0
    )
    return jsonify({
        "success": True,
        "message": "Demo session ready with ₹1,00,000 virtual capital and RELIANCE trend scenario.",
        **session.get_state()
    })


@quantlens_bp.route("/api/quantlens/autopilot/summary/<session_id>", methods=["GET"])
@quantlens_bp.route("/api/quantlens/autopilot/summary", methods=["GET"])
def api_autopilot_summary(session_id: str = ""):
    """Returns comprehensive performance KPIs, trade breakdown, and audit stats for the wrap-up report."""
    session = get_autopilot_session(session_id)
    if not session:
        return jsonify({"success": False, "error": f"Session '{session_id}' not found."}), 404
    return jsonify({"success": True, **session.get_summary()})


@quantlens_bp.route("/api/quantlens/autopilot/stream/<session_id>", methods=["GET"])
def api_autopilot_stream(session_id: str):
    """Server-Sent Events endpoint streaming continuous simulation steps."""
    session = get_autopilot_session(session_id)
    if not session:
        return jsonify({"success": False, "error": f"Session '{session_id}' not found."}), 404

    def event_stream():
        while session.status in ("RUNNING", "READY", "PAUSED"):
            if session.status == "RUNNING":
                session.step()
            state = session.get_state()
            yield f"data: {json.dumps(state)}\n\n"
            delay = max(0.2, 1.0 / max(0.5, session.playback_speed))
            time.sleep(delay)
            if session.status == "COMPLETED" and not session.loop_mode:
                yield f"data: {json.dumps(session.get_state())}\n\n"
                break

    return Response(event_stream(), mimetype="text/event-stream")


# =====================================================================
# XAI RESEARCH LAB & FACULTY MANDATE ENDPOINTS
# =====================================================================

@quantlens_bp.route("/api/quantlens/xai/feedback/perturb", methods=["GET", "POST"])
def api_xai_feedback_perturb():
    """
    Reverts explanation-selected features back into the model to evaluate score drop and prediction flip.
    Supports mean imputation, median imputation, zero imputation, and Gaussian noise.
    """
    from quantlens.xai_feedback import ExplanationFeedbackEngine
    data = (request.get_json(silent=True) or {}) if request.method == "POST" else request.args
    symbol = data.get("symbol", "RELIANCE")
    sample_idx = int(data.get("sample_idx", -1))
    target_date = data.get("target_date")
    model_family = data.get("model_family", "xgboost")
    explainer_type = data.get("explainer_type", "shap")
    k_features = int(data.get("k_features", 4))
    intervention = data.get("intervention", "mean_imputation")

    engine = ExplanationFeedbackEngine(symbol=symbol)
    res = engine.evaluate_feature_perturbation(
        sample_idx=sample_idx,
        target_date=target_date,
        model_family=model_family,
        explainer_type=explainer_type,
        k_features=k_features,
        intervention=intervention
    )
    return jsonify({"success": True, **res})


@quantlens_bp.route("/api/quantlens/xai/feedback/retrain-benchmark", methods=["GET", "POST"])
def api_xai_retrain_benchmark():
    """
    Compares 6 model variants retrained with feature selection subsets (Full vs SHAP vs LIME vs MI vs Random vs Ablation).
    """
    from quantlens.xai_feedback import ExplanationFeedbackEngine
    data = (request.get_json(silent=True) or {}) if request.method == "POST" else request.args
    symbol = data.get("symbol", "RELIANCE")
    k_features = int(data.get("k_features", 6))
    force_recompute = str(data.get("force_recompute", "false")).lower() in ("true", "1")

    engine = ExplanationFeedbackEngine(symbol=symbol)
    res = engine.run_retraining_benchmark(k_features=k_features, force_recompute=force_recompute)
    return jsonify({"success": True, **res})


@quantlens_bp.route("/api/quantlens/xai/feedback/cnn-gradcam", methods=["GET", "POST"])
def api_xai_cnn_gradcam_feedback():
    """
    Reverts Grad-CAM temporal explanations back into TimeSeriesConv1D.
    Masks peak salient temporal window vs control windows.
    """
    from quantlens.xai_feedback import ExplanationFeedbackEngine
    data = (request.get_json(silent=True) or {}) if request.method == "POST" else request.args
    symbol = data.get("symbol", "RELIANCE")
    target_date = data.get("target_date")
    mask_window_len = int(data.get("mask_window_len", 5))

    engine = ExplanationFeedbackEngine(symbol=symbol)
    res = engine.evaluate_cnn_gradcam_feedback(target_date=target_date, mask_window_len=mask_window_len)
    return jsonify({"success": True, **res})


@quantlens_bp.route("/api/quantlens/xai/metrics/comprehensive", methods=["GET", "POST"])
def api_xai_metrics_comprehensive():
    """
    Evaluates all 10 scientific XAI metrics: Stability, Consistency, Faithfulness, Fidelity,
    Robustness, Actionability, Confidence, Sensitivity, Sparsity, and Computational Cost.
    """
    from quantlens.xai_metrics import ScientificXAIEvaluator
    data = (request.get_json(silent=True) or {}) if request.method == "POST" else request.args
    symbol = data.get("symbol", "RELIANCE")
    n_samples = int(data.get("n_samples", 12))

    evaluator = ScientificXAIEvaluator(symbol=symbol)
    res = evaluator.evaluate_10_metrics(n_samples=n_samples)
    return jsonify({"success": True, **res})


@quantlens_bp.route("/api/quantlens/xai/sensitivity/sweep", methods=["GET", "POST"])
def api_xai_sensitivity_sweep():
    """
    Runs sensitivity experiments: input perturbation sweep, deletion curves, strategy parameters, and market regimes.
    """
    from quantlens.xai_sensitivity import SensitivityAnalysisLab
    data = (request.get_json(silent=True) or {}) if request.method == "POST" else request.args
    symbol = data.get("symbol", "RELIANCE")
    exp_type = data.get("experiment_type", "perturbation")

    lab = SensitivityAnalysisLab(symbol=symbol)
    if exp_type == "deletion":
        max_k = int(data.get("max_k", 6))
        res = lab.run_deletion_curves_comparison(max_k=max_k)
    elif exp_type == "strategy":
        res = lab.run_strategy_parameter_sensitivity()
    elif exp_type == "regime":
        res = lab.run_market_regime_sensitivity()
    else:
        sample_idx = int(data.get("sample_idx", -1))
        res = lab.run_input_perturbation_sweep(sample_idx=sample_idx)

    return jsonify({"success": True, **res})


@quantlens_bp.route("/api/quantlens/xai/gradcam/explain", methods=["GET", "POST"])
def api_xai_gradcam_explain():
    """
    Returns 1D Grad-CAM temporal heatmap, high-saliency intervals, and channel attributions for a date.
    """
    from quantlens.models_cnn import CNNModelManager
    from quantlens.xai_gradcam import GradCAMEngine
    data = (request.get_json(silent=True) or {}) if request.method == "POST" else request.args
    symbol = data.get("symbol", "RELIANCE")
    target_date = data.get("target_date")

    cnn_mgr = CNNModelManager(symbol=symbol)
    cnn_mgr.load_model()
    engine = GradCAMEngine(cnn_mgr)

    if target_date:
        res = engine.explain_by_date(target_date)
    else:
        last_window = cnn_mgr.X_all[-1] if cnn_mgr.X_all is not None else None
        if last_window is None:
            return jsonify({"success": False, "error": "CNN data not loaded"}), 400
        res = engine.explain_window(last_window)
        res["target_date"] = cnn_mgr.dates[-1] if cnn_mgr.dates else "latest"

    return jsonify({"success": True, **res})


@quantlens_bp.route("/api/quantlens/xai/actionability", methods=["GET", "POST"])
def api_xai_actionability():
    """
    Evaluates investor actionability ratio and classifies features into tunable parameters vs exogenous market state.
    """
    from quantlens.xai_feedback import ExplanationFeedbackEngine
    data = (request.get_json(silent=True) or {}) if request.method == "POST" else request.args
    symbol = data.get("symbol", "RELIANCE")
    engine = ExplanationFeedbackEngine(symbol=symbol)
    res = engine.evaluate_counterfactual_actionability(current_strategy_params={})
    return jsonify({"success": True, **res})


@quantlens_bp.route("/api/quantlens/xai/research/overview", methods=["GET"])
def api_xai_research_overview():
    """
    Consolidated scientific overview package for the XAI Research Lab dashboard.
    Returns Model A (XGBoost), Model B (PyTorch MLP), Model C (TimeSeriesConv1D) status,
    available explainers (SHAP, LIME, Grad-CAM), and MongoDB connection status.
    """
    from quantlens.ml_models import ModelManager
    from quantlens.models_cnn import CNNModelManager
    from quantlens.db_mongodb import get_mongodb
    symbol = request.args.get("symbol", "RELIANCE")

    model_mgr = ModelManager(symbol)
    model_mgr.load_models()

    cnn_mgr = CNNModelManager(symbol)
    cnn_mgr.load_model()

    db_mgr = get_mongodb()

    overview = {
        "success": True,
        "symbol": symbol.upper(),
        "models": {
            "model_a_xgboost": {
                "name": "XGBoost Classifier (Tree Ensemble)",
                "input_features": 22,
                "metrics": model_mgr.eval_metrics.get("xgboost", {})
            },
            "model_b_pytorch_mlp": {
                "name": "PyTorch MLP (3-Layer Neural Network)",
                "input_features": 22,
                "metrics": model_mgr.eval_metrics.get("pytorch_mlp", {})
            },
            "model_c_timeseries_cnn": {
                "name": "TimeSeriesConv1D (1D Temporal CNN)",
                "channels": 10,
                "lookback_window": 30,
                "metrics": cnn_mgr.eval_metrics
            }
        },
        "explainers": ["SHAP (TreeExplainer & Kernel)", "LIME (TabularExplainer)", "Grad-CAM (1D Temporal Saliency)"],
        "database": {
            "mongodb_connected": db_mgr.is_connected(),
            "database_name": db_mgr.db_name
        }
    }
    return jsonify(overview)



