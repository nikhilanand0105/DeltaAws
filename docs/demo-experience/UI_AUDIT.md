# QuantLens-XAI — Comprehensive UI and Backend Architecture Audit

## 1. Executive Summary

This audit assesses the current state of the **QuantLens-XAI** platform to establish the baseline for transforming the natural-language strategy execution journey into a world-class, cinematic, interactive AI strategy demonstration.

The underlying backend engines—including the local Ollama LLM integration, Pydantic strategy validation schema, deterministic event-driven backtesting engine, XGBoost & PyTorch MLP models, SHAP TreeExplainer, LIME TabularExplainer, Slide 9 evaluation metrics, Groww-inspired Paper Broker, and hybrid SQLite/MongoDB persistence—are **100% operational, real, and mathematically sound** (verified by the passing `tests/test_quantlens_complete_demo.py`).

However, the current frontend presentation relies on four disconnected, static tabs (`tab-builder`, `tab-backtest`, `tab-xai`, `tab-broker`) with manual navigation, basic button spinners, and static text lists. The critical journey **after the user enters a strategy and clicks RUN** is fragmented, requiring manual clicks across separate tabs.

---

## 2. Existing Screens and Interface Structure

The application serves the primary platform at `/quantlens` via `templates/quantlens.html`:

| Screen / Section | ID / Class | Existing Capabilities | Limitations / Deficiencies |
| :--- | :--- | :--- | :--- |
| **Academic Warning Banner** | `.academic-banner` | Discloses virtual paper-trading safety and local hardware runtime. | Static top strip; does not react to system status or presentation mode. |
| **Navigation Header** | `header` | Displays brand logo, model badge (`qwen2.5:0.5b`), and virtual fund badge. | Lacks Presentation Mode toggle, demo reset trigger, and quick navigation. |
| **Strategy Builder Tab** | `#tab-builder` | Plain English textarea, 3 preset buttons, "Compile & Verify Strategy" button, raw JSON schema display, 7-step static list (`#decisionTraceTimeline`), AI advisory card (`#advisoryContainer`). | No interactive rule extraction; no visual token mapping; no decision flowchart; no interactive risk panel; no cinematic loading or Mission Control view. |
| **Backtesting Tab** | `#tab-backtest` | Date inputs, Run Backtest button, 4 KPI cards (Cumulative Return, Sharpe, Drawdown, Win Rate), ApexCharts candlestick chart + RSI chart, trades table. | Static reveal; lacks replay controls (Play, Pause, 1x, 2x, 4x); no visual signal step-through; no animated numeric counters. |
| **Explainable AI Tab** | `#tab-xai` | Symbol & bar index selector, Fetch XAI button, XGBoost & PyTorch prediction summary, horizontal bar charts for SHAP and LIME, Slide 9 empirical evaluation metrics table. | Disconnected from strategy pipeline; lacks side-by-side ML Showdown; no interactive feature cross-linking across SHAP, LIME, and candlestick charts. |
| **Paper Broker Tab** | `#tab-broker` | Account summary cards (Cash, Invested, Portfolio Value, Unrealized P&L), replay button (60 bars), manual order form, positions table, orders ledger, audit log. | No cinematic deployment transition; replay lacks candle-by-candle animated order execution overlays; no portfolio count-up animation; no persistence inspector. |
| **Technical View / Inspector** | *Missing* | Backend has `/api/quantlens/db-status` for SQLite and MongoDB health. | Not exposed visually in the UI for database persistence proof. |
| **Final Results Screen** | *Missing* | End-of-run synthesis screen is absent. | Users are left on the broker tab without a unified closure screen or exportable report. |
| **Presentation Mode** | *Missing* | None. | UI has standard desktop density not optimized for 16:9 faculty demonstration or projector mode. |

---

## 3. Existing Backend APIs and Service Integration

| Endpoint | HTTP Method | Implementation Module | Current Functionality | Status & Event Capability |
| :--- | :--- | :--- | :--- | :--- |
| `/quantlens` | GET | `quantlens.routes` | Renders `quantlens.html` with initial paper broker state. | Active |
| `/api/quantlens/symbols` | GET | `quantlens.routes` | Returns supported historical symbols (`RELIANCE`, `TCS`, `INFY`, `NIFTY50`). | Active |
| `/api/quantlens/parse-strategy` | POST | `quantlens.llm_parser` | Invokes local Ollama (`qwen2.5:0.5b`) on Apple Silicon GPU; extracts typed Pydantic `StrategyDefinition`, 7-step decision trace, and AI advisory. | Active; synchronous response (~2.1s). |
| `/api/quantlens/validate-strategy` | POST | `quantlens.strategy_validator` | Validates against financial logic boundaries (fast < slow EMA, positive SL/TP, paper mode). | Active; synchronous (<5ms). |
| `/api/quantlens/backtest` | POST | `quantlens.backtest_engine` | Deterministic event-driven historical backtest on local OHLCV daily data; calculates Sharpe, Sortino, Drawdown, Win Rate, trades list, and candlestick overlays. | Active; synchronous (~150ms). |
| `/api/quantlens/xai-explain` | GET/POST | `quantlens.xai_engine` | Computes real SHAP TreeExplainer local values, LIME TabularExplainer local surrogate rules, and Slide 9 empirical evaluation metrics. | Active; synchronous (~800ms). |
| `/api/quantlens/paper-broker/dashboard` | GET | `quantlens.paper_broker` | Returns current virtual cash, invested equity, positions, order ledger, and immutable audit trail. | Active |
| `/api/quantlens/paper-broker/order` | POST | `quantlens.paper_broker` | Executes simulated market order with 0.05% brokerage fee and 0.05% slippage; enforces double-entry conservation in MongoDB. | Active |
| `/api/quantlens/paper-broker/replay` | POST | `quantlens.simulation_engine` | Replays 60 historical bars against the paper broker, generating real strategy-driven signals and fills. | Active; synchronous batch (~250ms). |
| `/api/quantlens/paper-broker/reset` | POST | `quantlens.paper_broker` | Resets virtual funds to ₹1,00,000 in memory and MongoDB. | Active |
| `/api/quantlens/models/status` | GET | `quantlens.routes` | Probes Ollama daemon and loads ML model metadata. | Active |
| `/api/quantlens/db-status` | GET | `quantlens.routes` | Reports SQLite table counts and MongoDB collection document counts. | Active |

---

## 4. State Management Analysis

### Frontend State
- Managed via global JS variables (`currentStrategy`, `candlestickChartInstance`, `rsiChartInstance`, `shapChartInstance`, `limeChartInstance`).
- Charts are recreated or updated on demand using ApexCharts.
- No central event bus or reactive state machine coordinates the 8 stages of strategy analysis.

### Backend State
- `PaperBroker` singleton (`quantlens/paper_broker.py`) maintains account balances and active positions.
- Data is dual-persisted:
  - Primary NoSQL: MongoDB database `quantlens_xai` (`paper_accounts`, `paper_orders`, `paper_positions`, `paper_trade_history`, `paper_audit_events`, `xai_evaluation_results`).
  - Relational SQL: SQLite database `instance/local.db` (`accounts`, `settings`, `strategies`, `strategy_states`, `trade_logs`, `local_signal_logs`).
- Deterministic seed fallback in `data/paper_broker_state.json` provides resilience if MongoDB is stopped.

---

## 5. Identified Gaps and Missing Interactions

1. **Disconnected Workflow:**
   Clicking "Compile & Verify Strategy" only updates two cards on the first tab. The user must manually notice the other tabs and click them one by one.
2. **Missing Strategy Intelligence Mission Control:**
   No full-screen or prominent modal command center exists to orchestrate the computation in real time.
3. **No Real-Time Progress Streaming (SSE):**
   The frontend makes discrete HTTP POST requests without a unified streaming progress mechanism (e.g. Server-Sent Events).
4. **No Animated Strategy Extraction:**
   The user prompt is not visually dissected into tokens (e.g. `10-DAY EMA` -> `Fast Moving Average`), and no interactive rule tree diagram is rendered.
5. **No Interactive Decision Flowchart:**
   The decision process is rendered as a plain HTML unordered list rather than an interactive node diagram allowing candle-by-candle inspection.
6. **No Risk Intelligence Panel:**
   Validation warnings and market regime warnings (e.g. choppy market whipsaw) are embedded in text paragraphs rather than structured, interactive risk cards with severity ratings (LOW / MODERATE / HIGH / CRITICAL) and actionable controls.
7. **No Contextual AI Strategy Advisor Q&A:**
   The AI advisory text is static; the user cannot ask follow-up questions to probe the rationale or explore parameter adjustments.
8. **No Visual Backtest Replay:**
   Backtest results are dumped immediately into a static chart and table rather than offering an interactive playback experience (Play, Pause, 1x, 2x, 4x, Next Signal).
9. **No Side-by-Side Model Showdown:**
   XGBoost and PyTorch MLP predictions are not compared head-to-head with explicit agreement/disagreement indicators.
10. **No Interactive XAI Cross-Linking:**
    Clicking a feature in the SHAP or LIME chart does not simultaneously highlight that indicator across the price chart, feature table, and explanation panel.
11. **No Cinematic Paper Broker Transition:**
    No animated deployment sequence bridges the approved strategy into the paper execution venue.
12. **No Simulated Trade Execution Animation:**
    Simulated trades during replay happen in an instant batch without candle pulsing, order submission overlays, fill receipts, or animated portfolio balance updates.
13. **No Technical View / System Inspector:**
    The dual SQLite + MongoDB architecture is not surfaced in an interactive inspector proving persistence.
14. **No Final Strategy Summary Screen:**
    The workflow lacks a comprehensive wrap-up dashboard summarizing strategy parameters, AI interpretation, model predictions, backtest KPIs, paper execution results, and XAI findings.
15. **No Faculty Presentation Mode:**
    There is no clean, 16:9 optimized fullscreen mode with step-by-step navigation and animation skip controls.

---

## 6. Required Backend Events and Progress Engine

To power the Mission Control interface, we need an event-driven analysis run orchestrator that emits standardized event payloads over **Server-Sent Events (SSE)** via:

`GET /api/quantlens/analysis-stream/<run_id>`

### Event Payload Schema:
```json
{
  "run_id": "run-1719500000",
  "strategy_id": "strat_reliance_1719500000",
  "stage": 1,
  "stage_name": "Natural Language Understanding",
  "status": "RUNNING | COMPLETED | CACHED | FAILED | NEEDS_CLARIFICATION",
  "timestamp": "2026-10-27T22:30:05.123Z",
  "title": "Local Ollama LLM Analyzing Strategy",
  "description": "Parsing natural language input using Qwen 2.5 on Apple Silicon GPU...",
  "progress_pct": 12.5,
  "discoveries": [
    {"type": "symbol", "label": "Symbol Detected", "value": "RELIANCE.NS"},
    {"type": "timeframe", "label": "Timeframe Detected", "value": "Daily"}
  ],
  "validation_summary": {"valid": true, "errors": [], "warnings": []},
  "data": {}
}
```

The 8 pipeline stages to be emitted are:
1. `STAGE 1: Natural Language Understanding` (LLM prompt tokenization & local model inference)
2. `STAGE 2: Strategy Extraction` (Structured parameters extraction & assumed defaults)
3. `STAGE 3: Rule Validation` (Pydantic schema check & mathematical boundary verification)
4. `STAGE 4: Risk Assessment` (Capital allocation, SL/TP presence, market regime scan)
5. `STAGE 5: Market Data Preparation` (Historical OHLCV data load & indicator calculation)
6. `STAGE 6: ML & XAI Analysis` (XGBoost vs PyTorch inference, SHAP & LIME computation)
7. `STAGE 7: Backtesting and Simulation` (Event-driven backtest & paper broker dry run)
8. `STAGE 8: Results Ready` (Complete analysis packaged for interactive exploration)

---

## 7. Performance and Hardware Constraints

- **Platform Target:** MacBook Pro M1 Pro, 16 GB Unified Memory.
- **Active Daemons:** Ollama (`qwen2.5:0.5b`), MongoDB 7.0, Flask backend, Web browser.
- **Design Guidelines:**
  - Leverage CSS hardware-accelerated transforms (`transform: translate3d(...)`, `opacity`) for 60fps animations.
  - Implement requestAnimationFrame for number counting and timeline progression.
  - Efficiently manage ApexCharts instances (destroy on unmount/re-render to prevent memory leaks).
  - Use non-blocking generators in Flask with immediate flushes for SSE delivery.
  - Support `prefers-reduced-motion` and an explicit "Skip Animations" toggle for fast demonstration.

---

## 8. Conclusion and Roadmap

The architecture is exceptionally solid at the data, ML, and execution levels. The required upgrade is entirely focused on creating an **extraordinary, cohesive, cinematic frontend experience** supported by a real-time progress streaming event system. We will proceed immediately to Phase 2 (Storyboarding and Animation Specification).
