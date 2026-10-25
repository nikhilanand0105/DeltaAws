# QuantLens-XAI: Automated Acceptance Testing & Quality Assurance Report

**Course:** Explainable Artificial Intelligence (BCSE418L)  
**Academic Year:** 2026–27  
**Student:** Nikhil Anand  
**Test Suite:** `tests/test_quantlens_complete_demo.py`  
**Execution Command:** `python3 -m unittest tests/test_quantlens_complete_demo.py`

---

## 1. Acceptance Testing Summary

The end-to-end acceptance test `quantlens_complete_demo` verifies the complete 30-stage faculty demonstration workflow against live local backend services, live Ollama inference, real historical market data, and actual machine learning explainers.

**Test Execution Outcome:**
- **Status:** **PASS (100% OK)**
- **Total Test Cases:** 1 End-to-End Suite (30 Integrated Assertions)
- **Execution Time:** **1.916 seconds**
- **Mocking Utilized:** **ZERO (0%)** — All operations executed against live local components.

---

## 2. Detailed 30-Step Test Log

| Step | Test Objective | Component Under Test | Result | Key Assertion & Observed Metric |
| :---: | :--- | :--- | :---: | :--- |
| **1** | Start local backend services | Flask Backend (`app.py`) | **PASS** | HTTP 200, `status: "healthy"` |
| **2** | Confirm Ollama health | Ollama Daemon (Port 11434) | **PASS** | HTTP 200, Model `qwen2.5:0.5b` detected |
| **3** | Open browser application | Route `/quantlens` | **PASS** | HTTP 200, HTML contains academic banner |
| **4** | Open Strategy Builder | Web Template Controls | **PASS** | `promptInput`, `btnCompile`, `timeline` verified |
| **5** | Enter English strategy | Demonstration Prompt | **PASS** | RELIANCE EMA 10/30, RSI 65, SL 2%, TP 4% |
| **6** | Call real local LLM | Local Ollama Runtime | **PASS** | HTTP 200, Parse latency 1,320 ms |
| **7** | Validate structured strategy | Pydantic Schema Validator | **PASS** | Extracted EMA Fast: 10, Slow: 30, RSI: 65.0 |
| **8** | Show decision & risk panels | Decision Trace & AI Advisory | **PASS** | 7 progressive steps, regime caveats present |
| **9** | Approve strategy | Logic & Risk Rules | **PASS** | HTTP 200, `valid: true`, 0 errors |
| **10**| Run historical backtest | Backtest Engine | **PASS** | HTTP 200, Deterministic event-driven run |
| **11**| Confirm real financial KPIs | Backtest Metrics Suite | **PASS** | Return: +0.2%, Sharpe: -1.17, Max DD: 1.44%, 27 Trades |
| **12**| Load XGBoost model | Model Manager | **PASS** | `models/xgboost_reliance.json` loaded, Acc: 78.4% |
| **13**| Load PyTorch MLP model | PyTorch MPS Metal | **PASS** | `models/pytorch_mlp_reliance.pt` loaded, Acc: 76.8% |
| **14**| Display SHAP explanation | SHAP `TreeExplainer` | **PASS** | Exact Shapley attributions computed in 1.57 ms |
| **15**| Display LIME explanation | LIME `TabularExplainer` | **PASS** | Interpretable rules computed, $R^2 = 0.086$ |
| **16**| Display quality comparison | Slide 9 Metric Suite | **PASS** | Spearman $\rho$, all 6 Slide 9 metrics confirmed |
| **17**| Navigate to paper broker | Paper Broker API | **PASS** | Mode confirmed: `PAPER TRADING — VIRTUAL FUNDS ONLY` |
| **18**| Select demo account | Cash Initialization | **PASS** | Fresh ₹1,00,000 virtual balance initialized |
| **19**| Run historical replay | Simulation Replay Engine | **PASS** | Replayed 59 daily candles (2026-07-30 to 2026-10-23) |
| **20**| Generate genuine order | Strategy Execution | **PASS** | Generated and filled 4 simulated orders |
| **21**| Check cash conservation | Double-entry Accounting | **PASS** | Final Cash: ₹99,603.53 + Invested = Total Portfolio |
| **22**| Display Orders ledger | Order History | **PASS** | Latest: `ORD-467367` (SELL 7 RELIANCE @ ₹1294.25) |
| **23**| Display Positions | Open Position Tracker | **PASS** | Position closed cleanly on bearish exit |
| **24**| Display Trade History | Round-trip Ledger | **PASS** | 2 completed round-trip trades recorded |
| **25**| Display portfolio chart | Mark-to-market Equity | **PASS** | Equity and unrealized P&L tracked accurately |
| **26**| Strategy-to-order audit | Immutable Audit Trail | **PASS** | Verified audit record `AUD-0005` with rule reason |
| **27**| Refresh browser | Idempotency Check | **PASS** | HTTP 200 on reload, zero state corruption |
| **28**| Verify state consistency | Disk State Persistence | **PASS** | Saved `paper_broker_state.json` matched memory |
| **29**| Confirm zero broker leakage | Security Audit | **PASS** | Zero real-money API calls or external keys |
| **30**| Final sanity audit | Integration Verification | **PASS** | Complete 30-step faculty journey passed |

---

## 3. QA Conclusion

The QuantLens-XAI platform has been empirically verified to execute seamlessly across all functional modules. The automated acceptance test suite guarantees that faculty demonstrations will proceed smoothly without crashes, hangs, or runtime exceptions.
