# QuantLens-XAI — Formal Trading Invariants & Mathematical Proofs

**System:** QuantLens-XAI  
**Author:** Nikhil Anand (24BCE1674)  
**Curriculum:** BCSE418L — Explainable Artificial Intelligence  
**Date:** October 28, 2026  
**Status:** ALL 30 INVARIANTS MATHEMATICALLY FORMALIZED & TESTED  

---

## 1. Introduction

In algorithmic trading, quantitative finance, and Explainable AI, system credibility depends entirely on mathematical rigor, absence of lookahead bias, strict double-entry conservation, and clear separation of concerns.

QuantLens-XAI establishes **30 non-negotiable architectural and trading invariants**. Every single invariant is enforced in code and backed by automated regression tests in `tests/test_quantlens_final_polish_30_invariants.py`.

---

## 2. Complete 30-Invariant Specification Matrix

| Invariant ID | Name | Mathematical / Logical Specification | Enforcement Mechanism | Test Method |
| :--- | :--- | :--- | :--- | :--- |
| **INV-01** | Model Confidence Boundedness | $\forall m \in \{\text{XGBoost}, \text{PyTorch}\}: \text{conf}(m) \in [0.0, 100.0]\%$ | `formatConfidence(val)` & probability argmax | `test_invariant_01_model_confidence_strictly_bounded` |
| **INV-02** | XAI Temporal Alignment | $Date(\text{Explanation}_t) \equiv Date(\text{Candle}_t)$ | `XAIEngine.explain_sample(target_date=...)` | `test_invariant_02_xai_temporal_alignment` |
| **INV-03** | Stop-Loss Precedence | If $P_t \le P_{\text{entry}} \times (1 - SL)$, emit SELL regardless of $P_{\text{ML}}(\text{BUY})$ | Risk boundary check precedes model signals | `test_invariant_03_stop_loss_precedence_over_bullish_model` |
| **INV-04** | Take-Profit Precedence | If $P_t \ge P_{\text{entry}} \times (1 + TP)$, emit SELL regardless of $P_{\text{ML}}(\text{BUY})$ | Profit harvest check precedes model signals | `test_invariant_04_take_profit_precedence_over_bullish_model` |
| **INV-05** | Reverse Crossover Exit | If $\text{EMA}_{\text{fast}} < \text{EMA}_{\text{slow}}$ and long position open, emit SELL | Trend reversal conditional trigger | `test_invariant_05_reverse_crossover_triggers_exit` |
| **INV-06** | Cash Conservation on BUY | $\text{Cash}_t = \text{Cash}_{t-1} - (Q \times P_{\text{fill}} + \text{Fee})$ | `PaperBroker.execute_order("BUY")` | `test_invariant_06_cash_conservation_on_buy` |
| **INV-07** | Cash Conservation on SELL | $\text{Cash}_t = \text{Cash}_{t-1} + (Q \times P_{\text{fill}} - \text{Fee})$ | `PaperBroker.execute_order("SELL")` | `test_invariant_07_cash_conservation_on_sell` |
| **INV-08** | Realized P&L Equals $\Delta \text{Cash}$ | $\sum \text{Net P\&L} \equiv \text{Cash}_{\text{final}} - \text{Cash}_{\text{initial}}$ (all positions closed) | Double-entry entry/exit friction tracking | `test_invariant_08_net_pnl_strictly_equals_delta_cash` |
| **INV-09** | Portfolio Valuation Identity | $\text{Total Equity}_t \equiv \text{Cash}_t + \sum_i (Q_i \times P_{i,t})$ | Mark-to-market accounting engine | `test_invariant_09_portfolio_valuation_identity` |
| **INV-10** | Insufficient Funds Rejection | If $(Q \times P_{\text{fill}} + \text{Fee}) > \text{Cash}_t \implies \text{Order Status} = \text{REJECTED}$ | Pre-trade capital solvency validation | `test_invariant_10_insufficient_funds_rejection` |
| **INV-11** | Max Position Limits | $\text{Count}(\text{Open Positions}) \le \text{Max Positions} (= 1)$ | Allocation rule guard | `test_invariant_11_max_position_limit_enforcement` |
| **INV-12** | Max Capital Allocation | $Q \times P_{\text{fill}} \le \text{Total Equity} \times \text{Max Alloc Pct} (\le 10\%)$ | Capped order sizing function | `test_invariant_12_max_allocation_limit_enforcement` |
| **INV-13** | Standardized Reason Codes | $\forall \text{order}: \text{reason\_code} \in \mathcal{S}_{\text{codes}}$ | Machine-readable reason enum assignment | `test_invariant_13_standardized_reason_codes_present` |
| **INV-14** | Three-Way Concept Separation | Response $\supset \{\text{model\_prediction}, \text{strategy\_decision}, \text{order\_execution}\}$ | Decoupled JSON data model | `test_invariant_14_three_way_separation_in_trade_explanation` |
| **INV-15** | Rule Precedence Notice | If $\text{Signal}_{\text{Strategy}} \neq \text{Signal}_{\text{ML}} \implies \text{Notice} \neq \emptyset$ | Architectural divergence synthesizer | `test_invariant_15_rule_precedence_notice_present` |
| **INV-16** | Data Feed Transparency | Mode $\equiv \text{PAPER TRADING (HISTORICAL REPLAY)}$ | Prominent UI telemetry banner | `test_invariant_16_data_feed_status_transparency` |
| **INV-17** | Candle Geometry Validity | $High \ge Low \land High \ge Open \land High \ge Close \land Low \le Open \land Low \le Close$ | OHLCV structural integrity validator | `test_invariant_17_candle_geometry_validity` |
| **INV-18** | Causal Step No Lookahead | $\text{Index}_{t+1} = \text{Index}_t + 1$ without future leakage | Sliced temporal window iterator | `test_invariant_18_causal_step_no_lookahead` |
| **INV-19** | Pause & Resume Idempotency | $\text{Step}(\text{Resume}(\text{Pause}(S))) \equiv \text{Step}(S)$ | Authoritative state machine transitions | `test_invariant_19_pause_and_resume_idempotency` |
| **INV-20** | Speed Throttling | $\text{Speed} \in [1x, 8x]$ | Simulation loop throttle multiplier | `test_invariant_20_playback_speed_throttling` |
| **INV-21** | Reset Restores Initial Capital | $\text{Reset}() \implies \text{Cash} = ₹1,00,000.00 \land \text{Positions} = \emptyset$ | Idempotent ledger reinitialization | `test_invariant_21_reset_restores_initial_capital` |
| **INV-22** | XGBoost Probability Axiom | $\sum_{c \in \{\text{SELL}, \text{HOLD}, \text{BUY}\}} P_{\text{XGB}}(c) = 1.0 \pm 0.001$ | Softmax / calibrated tree probability | `test_invariant_22_xgboost_probability_distribution_sums_to_one` |
| **INV-23** | PyTorch Probability Axiom | $\sum_{c \in \{\text{SELL}, \text{HOLD}, \text{BUY}\}} P_{\text{Torch}}(c) = 1.0 \pm 0.001$ | Torch Softmax layer output | `test_invariant_23_pytorch_probability_distribution_sums_to_one` |
| **INV-24** | SHAP Attribution Validity | $\forall \phi_i: \text{Feature}(\phi_i) \in \text{FEATURE\_COLUMNS}$ | `shap.TreeExplainer` attribution mapping | `test_invariant_24_shap_feature_attributions_validity` |
| **INV-25** | LIME Surrogate Fidelity | Local surrogate model weights bounded and evaluated | `lime.lime_tabular.LimeTabularExplainer` | `test_invariant_25_lime_local_surrogate_fidelity` |
| **INV-26** | Slippage Friction | $P_{\text{fill}}^{\text{BUY}} \ge P \land P_{\text{fill}}^{\text{SELL}} \le P$ | Non-negative slippage penalty ($0.05\%$) | `test_invariant_26_slippage_calculation_non_negative` |
| **INV-27** | Exact Brokerage Commission | $\text{Fee} = \text{Gross Value} \times 0.0005$ | Explicit turnover commission calculation | `test_invariant_27_brokerage_commission_calculation_exact` |
| **INV-28** | Win Rate Accounting | $\text{Win Rate} = \frac{\text{Count}(\text{Net P\&L} > 0)}{\text{Total Closed Trades}} \times 100\%$ | Closed trade ledger accounting | `test_invariant_28_win_rate_and_trade_accounting` |
| **INV-29** | Structured Activity Logging | $\forall e \in \text{Feed}: e \supset \{\text{type}, \text{title}, \text{detail}, \text{timestamp}\}$ | Typed telemetry emitter | `test_invariant_29_activity_feed_structured_logging` |
| **INV-30** | Zero Real Broker Leakage | $\text{External Network Requests to Real Brokers} \equiv 0$ | Virtual paper broker isolation sandbox | `test_invariant_30_zero_real_money_broker_leakage` |

---

## 3. Mathematical Proofs

### 3.1 Proof of Invariant 08 (Net P&L $\equiv \Delta \text{Cash}$)

**Theorem:** For any sequence of filled round-trip orders where all positions are liquidated, the cumulative reported Realized Net P&L strictly equals the net change in available cash.

**Proof:**
Let an initial position be opened with quantity $Q$ at market price $P_1$. With slippage $s$ and fee rate $f$:
$$\text{Fill Price}_{\text{buy}} = P_1 (1 + s)$$
$$\text{Gross Value}_{\text{buy}} = Q \cdot P_1 (1 + s)$$
$$\text{Fee}_{\text{buy}} = Q \cdot P_1 (1 + s) \cdot f$$
$$\text{Cash}_1 = \text{Cash}_0 - [\text{Gross Value}_{\text{buy}} + \text{Fee}_{\text{buy}}] = \text{Cash}_0 - Q \cdot P_1 (1 + s)(1 + f)$$

Let the position be liquidated at market price $P_2$:
$$\text{Fill Price}_{\text{sell}} = P_2 (1 - s)$$
$$\text{Gross Value}_{\text{sell}} = Q \cdot P_2 (1 - s)$$
$$\text{Fee}_{\text{sell}} = Q \cdot P_2 (1 - s) \cdot f$$
$$\text{Cash}_2 = \text{Cash}_1 + [\text{Gross Value}_{\text{sell}} - \text{Fee}_{\text{sell}}] = \text{Cash}_1 + Q \cdot P_2 (1 - s)(1 - f)$$

Subtracting $\text{Cash}_0$ from $\text{Cash}_2$:
$$\Delta \text{Cash} = \text{Cash}_2 - \text{Cash}_0 = Q \cdot P_2 (1 - s)(1 - f) - Q \cdot P_1 (1 + s)(1 + f)$$
$$= [Q \cdot P_2 (1 - s) - Q \cdot P_1 (1 + s)] - [\text{Fee}_{\text{buy}} + \text{Fee}_{\text{sell}}]$$
$$= \text{Gross P\&L} - \text{Total Friction} \equiv \text{Realized Net P\&L}$$

Thus, $\Delta \text{Cash} \equiv \text{Realized Net P\&L}$. $\blacksquare$

---

### 3.2 Proof of Invariant 03 & 15 (Risk Control Precedence)

**Theorem:** Algorithmic risk boundaries strictly supersede predictive model outputs under all financial market conditions.

**Proof:**
Let $S_t \in \{\text{BUY}, \text{HOLD}, \text{SELL}\}$ be the deterministic strategy action and $M_t = \arg\max_{c} P(c \mid X_t)$ be the ML model prediction.
The system execution function $\mathcal{F}$ is defined hierarchically:
$$\mathcal{F}(S_t, M_t) = \begin{cases} 
\text{SELL} & \text{if } \text{StopLossHit}(P_t) \lor \text{TakeProfitHit}(P_t) \\
\text{SELL} & \text{if } \text{ReversalCrossHit}(X_t) \\
\text{BUY} & \text{if } S_t = \text{BUY} \land \text{RiskPassed}(\text{Cash}_t) \\
\text{HOLD} & \text{otherwise}
\end{cases}$$

Since the risk predicate $\text{StopLossHit}(P_t)$ occupies the highest evaluation tier, if $\text{StopLossHit}(P_t) = \text{True}$, then $\mathcal{F} = \text{SELL}$, regardless of whether $M_t = \text{BUY}$ and $P(M_t) \to 1.0$.

When $M_t = \text{BUY}$ and $\mathcal{F} = \text{SELL}$, the system synthesizes a **Rule Precedence Active** notice explaining that deterministic capital preservation bounds override forward-looking speculative models. $\blacksquare$

---

## 4. Standardized Machine-Readable Reason Codes

QuantLens-XAI enforces a canonical dictionary of reason codes across all logs, orders, and UI badges:

- `ENTRY_EMA_CROSSOVER`: Bullish Golden Cross (Fast EMA crossed above Slow EMA).
- `ENTRY_RSI_CONFIRMED`: Golden Cross confirmed with RSI safely below exhaustion ceiling.
- `EXIT_STOP_LOSS`: Position liquidated due to price crossing stop-loss threshold.
- `EXIT_TAKE_PROFIT`: Position liquidated due to price achieving take-profit target.
- `EXIT_REVERSE_CROSSOVER`: Position liquidated due to Bearish Death Cross (Fast EMA < Slow EMA).
- `EXIT_SESSION_END`: Final candle of historical replay session reached.
- `HOLD_ENTRY_CONDITIONS_NOT_MET`: System scanning; entry criteria not yet satisfied.
- `HOLD_POSITION_OPEN`: Position active; trailing boundaries intact.
- `REJECT_INSUFFICIENT_FUNDS`: Virtual cash balance insufficient for minimum order size.
- `REJECT_POSITION_LIMIT`: Maximum concurrent position limit reached.
- `REJECT_ALLOCATION_LIMIT`: Order exceeds 10% maximum cash allocation boundary.
