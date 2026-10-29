# QUANTLENS-XAI: EVIDENCE MANIFEST & DATA PROVENANCE CATALOG
## Exhaustive Audit Trail for Figures, Tables, Models, and Experimental Artifacts

**Project:** QuantLens-XAI: An Explainable AI-Based Stock Market Recommendation and Risk Analysis System  
**Institution:** Vellore Institute of Technology (VIT)  
**Student:** Nikhil Anand (24BCE1674)  
**Course:** BCSE418L — Explainable Artificial Intelligence  
**Academic Year:** 2026–27  
**Canonical Evidence Ledger:** `subreports/evidence/EXPERIMENT_RESULTS.csv`  

---

## 1. EVIDENCE CATEGORY TAXONOMY

In accordance with strict academic integrity guidelines, all data points, tables, and figures in the final deliverables are categorized into three verified classifications:
1. **Measured Result (Real Application Output):** Produced directly by executing the underlying machine learning models, XAI explainers, perturbation engines, or test scripts on historical NSE market data. Zero fabrication.
2. **Real Application Screenshot:** Unaltered high-resolution capture of the live web terminal operating at `http://127.0.0.1:5001/quantlens`.
3. **Illustrative Demonstration / Proposed Protocol:** Clearly designated scenario or workflow diagram constructed to explain procedural interactions or pending human-in-the-loop expert protocols.

---

## 2. FIGURE MANIFEST & PROVENANCE MAPPING

| Figure ID | Deliverable Title | Source Path | Classification | Provenance & Execution Details |
| :--- | :--- | :--- | :--- | :--- |
| **Fig. 1** | System Overview & Architecture | `subreports/assets/architecture/arch_system_overview.png` | Real System Diagram | Reflects dual-flow engine in `quantlens/orchestrator.py` & `routes.py` |
| **Fig. 2** | Closed-Loop Feedback Flowchart | `subreports/assets/architecture/flow_closed_loop_feedback.png` | Methodological Diagram | Visualizes closed-loop feedback pipeline in `quantlens/xai_feedback.py` |
| **Fig. 3** | Baseline Model Performance | `subreports/assets/model_results/model_comparison_bars.png` | Measured Result | Evaluated on untouched 248-bar test split (`models_meta_reliance.json`) |
| **Fig. 4** | Retraining Leaderboard (Macro F1) | `subreports/assets/model_results/retraining_leaderboard_f1.png` | Measured Result | 6 retrained model variants from `quantlens/xai_feedback.py` |
| **Fig. 5** | 1D Grad-CAM Temporal Heatmap | `subreports/assets/xai_plots/gradcam_temporal_heatmap.png` | Measured Result | Computed from `conv3` layer of Model C (`quantlens/xai_gradcam.py`) |
| **Fig. 6** | Closed-Loop Score Drop (ΔP) | `subreports/assets/xai_plots/closed_loop_score_drop.png` | Measured Result | Top-4 SHAP drop (42.1%) vs Random (7.1%) vs Least (3.8%) |
| **Fig. 7** | Sequential Deletion AUC Curves | `subreports/assets/xai_plots/sequential_deletion_auc.png` | Measured Result | Progressive 6-step deletion curves for SHAP, LIME, Random, Bottom |
| **Fig. 8** | Perturbation Sweep Stability Decay | `subreports/assets/sensitivity/perturbation_sweep_decay.png` | Measured Result | Swept $\delta \in [0.1\%, 15\%]$ via `quantlens/xai_sensitivity.py` |
| **Fig. 9** | Market Volatility Regime Features | `subreports/assets/sensitivity/market_regime_features.png` | Measured Result | Low ATR vs High ATR feature attribution shifts |
| **Fig. 10** | Failure Case 1: Explainer Conflict | `subreports/assets/failure_cases/case1_explainer_disagreement.png` | Measured Result | Confirmed Spearman $\rho = -0.30$ on test candle |
| **Fig. 11** | Failure Case 2: Surrogate Underfit | `subreports/assets/failure_cases/case2_low_surrogate_fidelity.png` | Measured Result | LIME local surrogate $R^2 = 0.086$ on non-linear tree boundary |
| **Fig. 12** | Interactive Research Lab Interface | `subreports/assets/screenshots/01_xai_closed_loop_feedback.png` | Real App Screenshot | Live capture of Tab 09 3-panel closed-loop feedback UI |
| **Fig. 13** | Grad-CAM & 10-Metric UI Dashboard | `subreports/assets/screenshots/02_xai_gradcam_and_10_metrics.png` | Real App Screenshot | Live capture of 30-bar temporal heatmap & 10-metric table |
| **Fig. 14** | Sensitivity Lab & Leaderboard UI | `subreports/assets/screenshots/03_xai_sensitivity_and_retraining.png` | Real App Screenshot | Live capture of sensitivity curves & retraining leaderboard |
| **Fig. 15** | Faculty Viva Guide Interactive View | `subreports/assets/screenshots/04_xai_faculty_viva_guide.png` | Real App Screenshot | Live capture of 30-question interactive accordion in Tab 09 |
| **Fig. 16** | Strategy Composer Hero View | `subreports/assets/screenshots/05_strategy_builder_hero.png` | Real App Screenshot | Natural-language prompt compiler with local Ollama LLM |
| **Fig. 17** | Mission Control Telemetry View | `subreports/assets/screenshots/06_mission_control_cinematic.png` | Real App Screenshot | 8-stage SSE real-time strategy analysis orchestrator |
| **Fig. 18** | QuantLens Autopilot Cockpit | `subreports/assets/screenshots/07_autopilot_continuous_trading.png` | Real App Screenshot | Continuous paper trading engine with causal replay |
| **Fig. 19** | Paper Broker Portfolio Ledger | `subreports/assets/screenshots/08_paper_broker_portfolio.png` | Real App Screenshot | Groww-inspired virtual trading ledger with double-entry accounting |

---

## 3. TABLE MANIFEST & CROSS-REFERENCE

| Table ID | Table Title | Report Section | PPT Slide | Evidence ID |
| :--- | :--- | :--- | :--- | :--- |
| **Table 1** | Existing Studies, Tools & Research Comparison | Section 3 | Slide 4 | `LIT-COMP-01` |
| **Table 2** | Technical Indicators & Feature Dictionary | Section 5 | Slide 8 | `DATA-FEAT-01` |
| **Table 3** | Experimental Hardware & Software Setup | Section 6 | Slide 9 | `ENV-SETUP-01` |
| **Table 4** | Baseline Model Evaluation (Without XAI) | Section 7.1 | Slide 10 | `EXP-BASE-01..20` |
| **Table 5** | Closed-Loop Retraining Benchmark Leaderboard | Section 7.4 | Slide 18 | `EXP-RET-01..09` |
| **Table 6** | 10-Metric Scientific XAI Quality Evaluation | Section 7.5 | Slide 15 & 16 | `EXP-MET-01..27` |
| **Table 7** | Actionable vs Uncontrollable Feature Taxonomy | Section 7.5 | Slide 16 | `EXP-MET-16` |
| **Table 8** | Strategy Parameter Sensitivity Grid | Section 7.7 | Slide 17 | `EXP-SENS-01..03` |
| **Table 9** | Empirical Failure Case Diagnosis Matrix | Section 9 | Slide 19 | `FAIL-CASE-01..03` |
| **Table 10** | Faculty Requirements Compliance Matrix | Section 16 | Slide 22 | `COMPL-CHECK-01` |

---

## 4. DATABASE & ARTIFACT PROVENANCE AUDIT

Every numerical value reported in the project deliverables is verified against underlying persisted artifacts:
- **XGBoost Artifact:** `models/xgboost_reliance.json` (SHA-256 verified)
- **PyTorch MLP Artifact:** `models/pytorch_mlp_reliance.pt` (Torch state dict verified)
- **Model C CNN Artifact:** `models/pytorch_cnn_reliance.pt` (Torch state dict verified)
- **Model Metadata:** `models/models_meta_reliance.json` & `models/models_meta_cnn_reliance.json`
- **MongoDB Database:** `mongodb://localhost:27017/quantlens_xai`
  - Collection `xai_feedback_runs`: 12 verified documents
  - Collection `xai_retraining_benchmarks`: 1 verified benchmark document
  - Collection `xai_cnn_gradcam_runs`: 3 verified temporal mask runs
  - Collection `paper_orders`: 4 simulated orders with full audit provenance
