# QuantLens-XAI: Local LLM Integration & Strategy Parsing

## 1. Local LLM Architecture
QuantLens-XAI operates completely offline on Apple Silicon (M1 Pro) utilizing **Ollama** as the local inference runtime. Zero financial data, trading prompts, or API keys leave the user's workstation.

- **Primary Local Model**: `qwen2.5:0.5b` (or `qwen3.5:4b` when available)
- **Local Daemon Port**: `http://127.0.0.1:11434`
- **Context Window**: 4,096 tokens
- **Inference Latency**: $\approx 1,000\text{ ms}$ on 16 GB Apple Silicon Unified Memory
- **Cloud Dependency**: None ($0.00$ operational cost)

---

## 2. Prompt Engineering & Pydantic v2 Schema Enforcement
The LLM prompt is engineered to enforce strict JSON output adhering to the Pydantic v2 `TradingStrategySchema`:
- Extracts: `symbol`, `timeframe`, `indicators`, `entry_rules`, `exit_rules`, `risk_management` (`stop_loss_pct`, `take_profit_pct`, `max_capital_allocation_pct`).
- Robust Fallback: If local Ollama is offline or generates invalid syntax, an integrated regex and AST-based deterministic parser extracts parameters without failing the request.

---

## 3. Seven-Stage Visual Decision Trace
Every compilation produces an observable 7-stage decision trace displayed in the UI:
1. **Natural Language Input**: User prompt ingestion and sanitization.
2. **LLM Tokenization & Intent Extraction**: Parameter isolation (symbol, moving average periods, risk parameters).
3. **Pydantic Schema Validation**: Structural validation with type checking and bounds enforcement.
4. **Technical Indicator Alignment**: Mapping rules to real computation engines (e.g. EMA 10/30, RSI 14).
5. **Risk Boundary Verification**: Enforcement of hard limits (e.g., maximum stop loss $\le 10\%$, allocation $\le 50\%$).
6. **Execution Feasibility Check**: Verification of symbol market availability in local datasets.
7. **AI Advisory Formulation**: Synthesis of confidence score, risk category, and plain-English recommendations.
