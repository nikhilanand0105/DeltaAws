# QUANTLENS-XAI: FACULTY REQUIREMENTS TRACEABILITY MATRIX
## Comprehensive Compliance Checklist for VIT Explainable Artificial Intelligence (BCSE418L)

**Student:** Nikhil Anand (24BCE1674)  
**Institution:** Vellore Institute of Technology (VIT)  
**Submission Deadline:** October 12th to 30th, 2026  
**Primary Review Date:** 28 October 2026  

---

## 1. TEACHER'S EXACT MANDATE COMPLIANCE MATRIX

| # | Teacher's Exact Requirement | Project Report Section | PowerPoint Slide | README Section | Evidence & Artifact Location | Compliance Status |
| :-: | :--- | :--- | :--- | :--- | :--- | :---: |
| **1** | *"Not just stop with LIME/ SHAP/ GradCAM explanation."* | Abstract, Sec. 1, Sec. 2 | Slide 2, 3, 5 | Sec. 1, Sec. 3 | `quantlens/xai_feedback.py` | **100% COMPLIANT** |
| **2** | *"revert the explanation generated into the models involved again"* | Sec. 4, Sec. 6, Sec. 7.3 | Slide 7, 13, 14 | Sec. 4, Sec. 15 | `evaluate_feature_perturbation()` | **100% COMPLIANT** |
| **3** | *"evaluate the performance with xai metrics and compare."* | Sec. 7.4, Sec. 7.5, Sec. 7.8 | Slide 15, 16, 18 | Sec. 5, Sec. 16 | `evaluate_10_metrics()` | **100% COMPLIANT** |
| **4** | *"Such as stability"* | Sec. 7.5 (Metric 1) | Slide 15, 16 | Sec. 16 | Cosine Sim under 0.05σ (SHAP: 0.941) | **100% COMPLIANT** |
| **5** | *"consistency"* | Sec. 7.5 (Metric 2) | Slide 15, 16 | Sec. 16 | Spearman ρ = 0.352, Jaccard = 0.40 | **100% COMPLIANT** |
| **6** | *"faithfulness"* | Sec. 7.3, Sec. 7.5 (Metric 3) | Slide 13, 15 | Sec. 15, Sec. 16 | Deletion AUC, Drop Ratio 5.9x | **100% COMPLIANT** |
| **7** | *"fidelity"* | Sec. 7.5 (Metric 4) | Slide 15, 16 | Sec. 16 | SHAP Additivity (1.0), LIME R² (0.887) | **100% COMPLIANT** |
| **8** | *"robustness"* | Sec. 7.5 (Metric 5) | Slide 15, 16 | Sec. 16 | High vs Low ATR Invariance (0.880) | **100% COMPLIANT** |
| **9** | *"actionability"* | Sec. 7.5 (Metric 6) | Slide 16, 17 | Sec. 16 | 40.9% Actionable Strategy Features | **100% COMPLIANT** |
| **10** | *"confidence, etc..."* | Sec. 7.5 (Metric 7, 8, 9, 10)| Slide 15, 16 | Sec. 16 | ECE=0.124, Entropy, Sensitivity, Gini | **100% COMPLIANT** |
| **11** | *"Include sensitivity analysis."* | Sec. 7.7 (Results & Disc.) | Slide 17 | Sec. 17 | 4 Experiment Families | **100% COMPLIANT** |
| **12** | *"Report submission in lms (doc)"* | `QuantLens_XAI_Final_Project_Report.docx` | Full Deck | Sec. 1, Sec. 26 | `subreports/` folder | **100% COMPLIANT** |
| **13** | *"ppt, readme file"* | `QuantLens_XAI_Final_Review.pptx` & `README.md` | Full Deck | Full File | `subreports/` folder | **100% COMPLIANT** |

---

## 2. REPORT CONTENT & CHAPTER COMPLIANCE CHECKLIST

| Teacher Required Content | Present in DOCX Report | Present in PPT | Present in README | Verification Detail | Status |
| :--- | :---: | :---: | :---: | :--- | :---: |
| **Abstract** | Section 1 | Slide 1 | Section 2 | Summarizes closed-loop feedback, Model C CNN, metrics | **VERIFIED** |
| **Introduction** | Section 2 | Slide 2 | Section 2 | Motivation, black-box risks, problem statement | **VERIFIED** |
| **Comparison table of relevant existing study of tools and research works** | Section 3 (Table 1) | Slide 4 | Section 3 | 10 verified academic studies & tools (Quantus, Captum) | **VERIFIED** |
| **Research gap analysis** | Section 3.2 | Slide 5 | Section 3 | Distinguishes open-loop visualization from closed-loop validation | **VERIFIED** |
| **Proposed architecture/framework - diagram and procedural steps** | Section 4 (Fig. 1 & 2) | Slide 6 & 7 | Section 7 | System diagram & 9-step procedural feedback workflow | **VERIFIED** |
| **Dataset description** | Section 5 (Table 2) | Slide 8 | Section 12 | 1,687 daily candles, 22 features, chronological splits | **VERIFIED** |
| **Experimental setup** | Section 6 (Table 3) | Slide 9 | Section 9, 10 | M1 Pro Metal GPU, PyTorch 2.8, Scikit-Learn, SHAP | **VERIFIED** |
| **Result and discussion with base model separately** | Section 7.1 (Table 4) | Slide 10 | Section 13 | Separate evaluation: XGBoost vs MLP vs TimeSeriesConv1D | **VERIFIED** |
| **Model using XAI - various scenarios** | Section 7.2 | Slide 11 & 12 | Section 14 | Local SHAP waterfalls, LIME rules, Grad-CAM heatmaps | **VERIFIED** |
| **Explanation feedback into models** | Section 7.3 (Fig. 6) | Slide 13 & 14 | Section 15 | Score drop ΔP, decision flips, Random/Least controls | **VERIFIED** |
| **Retraining benchmark with XAI feature selection** | Section 7.4 (Table 5) | Slide 18 | Section 15 | Full vs SHAP (0.341 F1) vs Random vs MI vs Ablation | **VERIFIED** |
| **Plots and figures of analysis wrt various features and metrics** | Section 7.5 (Table 6) | Slide 15 & 16 | Section 16 | 10 academic metrics with explicit mathematical formulas | **VERIFIED** |
| **Sensitivity analysis in result section** | Section 7.7 (Fig. 8 & 9)| Slide 17 | Section 17 | Noise sweeps, deletion curves, strategy grid, regimes | **VERIFIED** |
| **If IML involved, require human expert feedback** | Section 8 | Slide 20 | Section 23 | Rigorous academic distinction: post-hoc XAI vs IML | **VERIFIED** |
| **Observation on failure cases outcome with XAI result and discussion** | Section 9 (Table 9) | Slide 19 | Section 23 | Case 1: Explainer conflict; Case 2: Surrogate underfit | **VERIFIED** |
| **Novel Contributions in the work - pointwise** | Section 10 | Slide 21 | Section 5 | 8 pointwise, defensible methodological contributions | **VERIFIED** |
| **Conclusion** | Section 11 | Slide 22 | Section 24 | Synthesizes findings, limitations, future research | **VERIFIED** |
| **References** | Section 12 | Slide 23 | Section 25 | 14 verified, non-hallucinated peer-reviewed citations | **VERIFIED** |

---

## 3. SUMMARY OF DELIVERABLES IN `subreports/`

1. **Academic Word Document:** `subreports/QuantLens_XAI_Final_Project_Report.docx`  
   - Generated using `python-docx` with professional styles, heading hierarchies, table borders, and callouts.
2. **Revised Research PowerPoint:** `subreports/QuantLens_XAI_Final_Review.pptx`  
   - Rebuilt from original deck into 23 focused slides + appendix with complete speaker notes and visual assets.
3. **Comprehensive README:** `subreports/README.md`  
   - Exhaustive technical manual with verified setup commands, architecture flows, and demo walkthrough.
4. **Canonical Evidence Ledger:** `subreports/evidence/EXPERIMENT_RESULTS.csv`  
   - 60+ verified numerical entries forming the single source of truth.
5. **Evidence Manifest:** `subreports/evidence/EVIDENCE_MANIFEST.md`  
   - Detailed mapping of every figure and table to its provenance file.
6. **Original Presentation Backup:** `subreports/archive/original_presentation_backup.pptx`  
   - Original 16-slide presentation safely preserved.
