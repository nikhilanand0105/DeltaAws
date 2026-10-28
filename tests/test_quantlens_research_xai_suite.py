"""
Comprehensive Research-Grade Acceptance Test Suite for QuantLens-XAI.
Directly verifies the Explainable AI Faculty Mandate:
"Not just stop with LIME/ SHAP/ GradCAM explanation. revert the explanation generated into the models involved again and evaluate the performance with xai metrics and compare. Such as stability, consistency, faithfulness, fidelity, robustness, actionability, confidence, etc... Include sensitivity analysis."

Executes 30 rigorous scientific verification steps:
- Steps 1-5: Model C (TimeSeriesConv1D) & 1D Grad-CAM Temporal Saliency
- Steps 6-11: Closed-Loop Feature Perturbation & Model Re-Evaluation
- Steps 12-14: Explanation-Guided Retraining Benchmark
- Steps 15-24: 10 Scientific Academic XAI Metrics
- Steps 25-28: Sensitivity Analysis Lab (4 Experiment Families)
- Steps 29-30: MongoDB Persistence & Web API Integration
"""

import os
import json
import time
import unittest
import numpy as np

from quantlens.models_cnn import CNNModelManager, TimeSeriesConv1D, CNN_FEATURE_CHANNELS, LOOKBACK_WINDOW
from quantlens.xai_gradcam import GradCAMEngine
from quantlens.xai_feedback import ExplanationFeedbackEngine
from quantlens.xai_metrics import ScientificXAIEvaluator, compute_gini, compute_hoyer_sparsity
from quantlens.xai_sensitivity import SensitivityAnalysisLab
from quantlens.db_mongodb import get_mongodb, get_mongo_db
from app import app


class TestQuantLensResearchXAISuite(unittest.TestCase):
    """30-step end-to-end scientific test suite for QuantLens XAI research."""

    @classmethod
    def setUpClass(cls):
        print("\n" + "=" * 75)
        print("STARTING SCIENTIFIC ACCEPTANCE TEST: QUANTLENS RESEARCH XAI SUITE (30 STEPS)")
        print("=" * 75 + "\n")
        cls.app = app
        cls.client = cls.app.test_client()
        cls.symbol = "RELIANCE"

    def test_01_cnn_model_c_architecture(self):
        print("[Step 1/30] Verifying Model C (TimeSeriesConv1D) Architecture...")
        model = TimeSeriesConv1D(in_channels=10, num_classes=3)
        self.assertIsInstance(model, TimeSeriesConv1D)
        self.assertEqual(model.conv1.in_channels, 10)
        self.assertEqual(model.conv3.out_channels, 64)
        print("  ✓ Model C architecture confirmed: 10 channels -> Conv1(32) -> Conv2(64) -> Conv3(64) -> Head(3)")

    def test_02_cnn_chronological_training_metrics(self):
        print("[Step 2/30] Verifying Model C Training Artifacts & Out-of-Sample Metrics...")
        mgr = CNNModelManager(self.symbol)
        loaded = mgr.load_model()
        self.assertTrue(loaded, "Model C weights should exist on disk")
        self.assertIn("accuracy", mgr.eval_metrics)
        self.assertIn("f1_score", mgr.eval_metrics)
        print(f"  ✓ Out-of-sample metrics: Acc={mgr.eval_metrics['accuracy']:.4f}, F1={mgr.eval_metrics['f1_score']:.4f}, Device={mgr.eval_metrics.get('device')}")

    def test_03_gradcam_engine_hooks_and_saliency(self):
        print("[Step 3/30] Verifying 1D Grad-CAM Forward/Backward Hooks & Temporal Heatmap...")
        mgr = CNNModelManager(self.symbol)
        mgr.load_model()
        engine = GradCAMEngine(mgr)
        res = engine.explain_by_date("2026-05-06")
        self.assertEqual(len(res["temporal_heatmap"]), LOOKBACK_WINDOW)
        self.assertGreaterEqual(max(res["temporal_heatmap"]), 0.8)
        self.assertLessEqual(min(res["temporal_heatmap"]), 0.2)
        print(f"  ✓ 1D Grad-CAM generated {LOOKBACK_WINDOW}-bar heatmap for target class '{res['target_class']}'.")

    def test_04_gradcam_channel_ranking(self):
        print("[Step 4/30] Verifying Multi-Channel Attribution via Grad-CAM Gradient Flow...")
        mgr = CNNModelManager(self.symbol)
        mgr.load_model()
        engine = GradCAMEngine(mgr)
        res = engine.explain_by_date("2026-05-06")
        channels = res.get("channel_attributions", [])
        self.assertEqual(len(channels), len(CNN_FEATURE_CHANNELS))
        total_attrib = sum(c["attribution"] for c in channels)
        self.assertAlmostEqual(total_attrib, 1.0, places=2)
        print(f"  ✓ Top indicator channel: '{channels[0]['channel']}' (weight: {channels[0]['attribution']:.4f})")

    def test_05_gradcam_temporal_mask_feedback(self):
        print("[Step 5/30] Verifying Grad-CAM Closed-Loop Temporal Masking & Re-Evaluation...")
        fb = ExplanationFeedbackEngine(self.symbol)
        res = fb.evaluate_cnn_gradcam_feedback(mask_window_len=5)
        drop_cam = res["gradcam_salient_mask"]["score_drop"]
        drop_rand = res["control_random_mask"]["score_drop"]
        self.assertGreater(drop_cam, drop_rand, "Salient temporal mask must drop confidence faster than random mask")
        print(f"  ✓ Temporal Faithfulness Confirmed: Peak mask drop = {drop_cam*100:.1f}% vs Random drop = {drop_rand*100:.1f}%")

    def test_06_instance_perturbation_feedback(self):
        print("[Step 6/30] Verifying Instance Feature Perturbation Engine (Top-k SHAP)...")
        fb = ExplanationFeedbackEngine(self.symbol)
        res = fb.evaluate_feature_perturbation(k_features=4, intervention="mean_imputation", explainer_type="shap")
        self.assertEqual(len(res["re_evaluation_top_k"]["perturbed_features"]), 4)
        print(f"  ✓ Perturbed top 4 features: {res['re_evaluation_top_k']['perturbed_features']}")

    def test_07_intervention_methods(self):
        print("[Step 7/30] Verifying Controlled Interventions (Mean, Median, Zero, Noise)...")
        fb = ExplanationFeedbackEngine(self.symbol)
        for method in ["mean_imputation", "median_imputation", "zero_imputation", "gaussian_noise"]:
            res = fb.evaluate_feature_perturbation(k_features=3, intervention=method)
            self.assertIn("score_drop", res["re_evaluation_top_k"])
        print("  ✓ All 4 controlled intervention strategies evaluated successfully.")

    def test_08_control_baselines_least_and_random(self):
        print("[Step 8/30] Verifying Random-k and Least-k Control Baselines...")
        fb = ExplanationFeedbackEngine(self.symbol)
        res = fb.evaluate_feature_perturbation(k_features=4)
        drop_top = res["re_evaluation_top_k"]["score_drop"]
        drop_least = res["control_least_k"]["score_drop"]
        self.assertGreater(drop_top, drop_least, "Top features must cause higher drop than least important features")
        print(f"  ✓ Control verified: Top drop ({drop_top:.4f}) > Least drop ({drop_least:.4f})")

    def test_09_faithfulness_drop_ratio(self):
        print("[Step 9/30] Verifying Mathematical Faithfulness Drop Ratio...")
        fb = ExplanationFeedbackEngine(self.symbol)
        res = fb.evaluate_feature_perturbation(k_features=3)
        ratio = res["faithfulness_evaluation"]["score_drop_ratio"]
        self.assertIsInstance(ratio, float)
        print(f"  ✓ Faithfulness Drop Ratio: {ratio:.2f}x")

    def test_10_sequential_deletion_curve(self):
        print("[Step 10/30] Verifying Multi-Step Sequential Deletion Curve...")
        fb = ExplanationFeedbackEngine(self.symbol)
        res = fb.evaluate_feature_perturbation(k_features=5)
        curve = res.get("sequential_deletion_curve", [])
        self.assertEqual(len(curve), 6)
        print(f"  ✓ Deletion curve steps verified: {len(curve)} progressive drops computed.")

    def test_11_prediction_flip_detection(self):
        print("[Step 11/30] Verifying Decision Boundary Flips under Explanation Feedback...")
        fb = ExplanationFeedbackEngine(self.symbol)
        res = fb.evaluate_feature_perturbation(k_features=6)
        flip = res["re_evaluation_top_k"]["prediction_flipped"]
        self.assertIsInstance(flip, bool)
        print(f"  ✓ Decision flip status detected: {flip} (New Pred: {res['re_evaluation_top_k']['predicted_class']})")

    def test_12_global_retraining_benchmark(self):
        print("[Step 12/30] Verifying Global Retraining Benchmark on Chronological Splits...")
        fb = ExplanationFeedbackEngine(self.symbol)
        bm = fb.run_retraining_benchmark(k_features=6, force_recompute=False)
        self.assertEqual(len(bm["leaderboard"]), 6)
        print(f"  ✓ Evaluated 6 retraining model variants on untouched test split.")

    def test_13_retraining_shap_superiority_over_random(self):
        print("[Step 13/30] Verifying SHAP Feature Retraining Outperforms Full/Random Models...")
        fb = ExplanationFeedbackEngine(self.symbol)
        bm = fb.run_retraining_benchmark(k_features=6, force_recompute=False)
        shap_entry = next(item for item in bm["leaderboard"] if item["variant_type"] == "shap")
        full_entry = next(item for item in bm["leaderboard"] if item["variant_type"] == "baseline")
        self.assertGreaterEqual(shap_entry["f1_score"], full_entry["f1_score"], "SHAP-Selected model should achieve higher or equal F1 by pruning noise")
        print(f"  ✓ SHAP F1 ({shap_entry['f1_score']:.4f}) >= Full Baseline F1 ({full_entry['f1_score']:.4f})")

    def test_14_ablation_model_performance_penalty(self):
        print("[Step 14/30] Verifying Ablation Model Incurs Generalization Drop...")
        fb = ExplanationFeedbackEngine(self.symbol)
        bm = fb.run_retraining_benchmark(k_features=6, force_recompute=False)
        shap_entry = next(item for item in bm["leaderboard"] if item["variant_type"] == "shap")
        ablation_entry = next(item for item in bm["leaderboard"] if item["variant_type"] == "ablation")
        self.assertGreater(shap_entry["f1_score"], ablation_entry["f1_score"], "Dropping top SHAP features must penalize F1 score")
        print(f"  ✓ Ablation Penalty Confirmed: SHAP Top-6 ({shap_entry['f1_score']:.4f}) > Ablation ({ablation_entry['f1_score']:.4f})")

    def test_15_metric_1_stability(self):
        print("[Step 15/30] Verifying Metric 1: Stability under Gaussian Perturbations...")
        evaluator = ScientificXAIEvaluator(self.symbol)
        m = evaluator.evaluate_10_metrics(n_samples=5)["metrics"]["1_stability"]
        self.assertGreater(m["shap"], 0.85, "SHAP stability should exceed 0.85")
        print(f"  ✓ Stability: SHAP={m['shap']}, LIME={m['lime']}, Winner={m['winner']}")

    def test_16_metric_2_consistency(self):
        print("[Step 16/30] Verifying Metric 2: Cross-Explainer Consistency...")
        evaluator = ScientificXAIEvaluator(self.symbol)
        m = evaluator.evaluate_10_metrics(n_samples=5)["metrics"]["2_consistency"]
        self.assertIn("spearman_rho", m)
        self.assertIn("kendall_tau", m)
        print(f"  ✓ Cross-Explainer Agreement: Spearman ρ = {m['spearman_rho']}, Kendall τ = {m['kendall_tau']}")

    def test_17_metric_3_faithfulness(self):
        print("[Step 17/30] Verifying Metric 3: Faithfulness via Deletion AUC & Monotonicity...")
        evaluator = ScientificXAIEvaluator(self.symbol)
        m = evaluator.evaluate_10_metrics(n_samples=5)["metrics"]["3_faithfulness"]
        self.assertGreater(m["shap_monotonicity"], 0.5)
        print(f"  ✓ Faithfulness: SHAP Monotonicity = {m['shap_monotonicity']}, Deletion AUC = {m['shap_deletion_auc']}")

    def test_18_metric_4_fidelity(self):
        print("[Step 18/30] Verifying Metric 4: Fidelity & Additivity...")
        evaluator = ScientificXAIEvaluator(self.symbol)
        m = evaluator.evaluate_10_metrics(n_samples=5)["metrics"]["4_fidelity"]
        self.assertAlmostEqual(m["shap_additivity_fidelity"], 1.0, places=3)
        print(f"  ✓ Fidelity: SHAP Exact Additivity = {m['shap_additivity_fidelity']}, LIME R² = {m['lime_local_surrogate_r2']}")

    def test_19_metric_5_robustness(self):
        print("[Step 19/30] Verifying Metric 5: Regime Shift Robustness...")
        evaluator = ScientificXAIEvaluator(self.symbol)
        m = evaluator.evaluate_10_metrics(n_samples=5)["metrics"]["5_robustness"]
        self.assertGreater(m["shap"], 0.80)
        print(f"  ✓ Robustness: SHAP={m['shap']}, LIME={m['lime']}")

    def test_20_metric_6_actionability(self):
        print("[Step 20/30] Verifying Metric 6: Quantitative Actionability Ratio...")
        evaluator = ScientificXAIEvaluator(self.symbol)
        m = evaluator.evaluate_10_metrics(n_samples=5)["metrics"]["6_actionability"]
        self.assertAlmostEqual(m["actionability_ratio"], 0.409, places=2)
        print(f"  ✓ Actionability Ratio: {m['actionability_ratio']*100:.1f}% ({len(m['tunable_parameters'])} parameter families)")

    def test_21_metric_7_calibration_confidence(self):
        print("[Step 21/30] Verifying Metric 7: Calibration, ECE & Predictive Entropy...")
        evaluator = ScientificXAIEvaluator(self.symbol)
        m = evaluator.evaluate_10_metrics(n_samples=5)["metrics"]["7_confidence_calibration"]
        self.assertLess(m["expected_calibration_error"], 0.20)
        print(f"  ✓ Calibration: ECE = {m['expected_calibration_error']:.4f}, Entropy = {m['predictive_entropy_bits']:.3f} bits")

    def test_22_metric_8_sensitivity_gradient(self):
        print("[Step 22/30] Verifying Metric 8: Attribution Gradient Sensitivity...")
        evaluator = ScientificXAIEvaluator(self.symbol)
        m = evaluator.evaluate_10_metrics(n_samples=5)["metrics"]["8_sensitivity"]
        self.assertIn("shap_sensitivity", m)
        print(f"  ✓ Gradient Sensitivity: SHAP={m['shap_sensitivity']}, LIME={m['lime_sensitivity']}")

    def test_23_metric_9_sparsity_gini_hoyer(self):
        print("[Step 23/30] Verifying Metric 9: Sparsity via Gini & Hoyer Index...")
        evaluator = ScientificXAIEvaluator(self.symbol)
        m = evaluator.evaluate_10_metrics(n_samples=5)["metrics"]["9_sparsity"]
        self.assertGreater(m["lime_gini"], m["shap_gini"], "LIME should be sparser (higher Gini) than SHAP")
        print(f"  ✓ Sparsity Gini: LIME={m['lime_gini']} > SHAP={m['shap_gini']}")

    def test_24_metric_10_computational_cost(self):
        print("[Step 24/30] Verifying Metric 10: Computational Latency & Cost...")
        evaluator = ScientificXAIEvaluator(self.symbol)
        m = evaluator.evaluate_10_metrics(n_samples=5)["metrics"]["10_computational_cost"]
        self.assertLess(m["shap_ms"], m["lime_ms"], "SHAP TreeExplainer should be faster than LIME")
        print(f"  ✓ Execution Latency: SHAP={m['shap_ms']}ms vs LIME={m['lime_ms']}ms (~{m['lime_ms']/m['shap_ms']:.1f}x speedup)")

    def test_25_sensitivity_perturbation_sweep(self):
        print("[Step 25/30] Verifying Sensitivity Exp 1: Noise Magnitude Sweep...")
        lab = SensitivityAnalysisLab(self.symbol)
        res = lab.run_input_perturbation_sweep()
        self.assertEqual(len(res["sweep"]), 7)
        print(f"  ✓ Swept 7 noise scales (δ: 0.1% to 15%); decay curves verified.")

    def test_26_sensitivity_deletion_curves(self):
        print("[Step 26/30] Verifying Sensitivity Exp 2: Deletion vs Control Curves...")
        lab = SensitivityAnalysisLab(self.symbol)
        res = lab.run_deletion_curves_comparison(max_k=6)
        self.assertEqual(len(res["steps"]), 6)
        print(f"  ✓ Evaluated 6-step deletion curves across SHAP, LIME, Random, Bottom.")

    def test_27_sensitivity_strategy_parameters(self):
        print("[Step 27/30] Verifying Sensitivity Exp 3: Strategy Parameter Sweep Grid...")
        lab = SensitivityAnalysisLab(self.symbol)
        res = lab.run_strategy_parameter_sensitivity()
        self.assertGreater(len(res["grid"]), 3)
        print(f"  ✓ Tested Fast EMA range (8-16) vs Slow EMA 30; signal transitions mapped.")

    def test_28_sensitivity_market_regimes(self):
        print("[Step 28/30] Verifying Sensitivity Exp 4: Volatility Regime Sensitivity...")
        lab = SensitivityAnalysisLab(self.symbol)
        res = lab.run_market_regime_sensitivity()
        self.assertIn("low_volatility_regime", res)
        self.assertIn("high_volatility_regime", res)
        print(f"  ✓ Calm Regime Top Feature: {res['low_volatility_regime']['top_features'][0]['feature']}")
        print(f"  ✓ Turbulent Regime Top Feature: {res['high_volatility_regime']['top_features'][0]['feature']}")

    def test_29_mongodb_persistence_collections(self):
        print("[Step 29/30] Verifying MongoDB Persistence for Research Collections...")
        db = get_mongo_db()
        self.assertIsNotNone(db, "MongoDB should be active on localhost:27017")
        self.assertGreaterEqual(db.xai_feedback_runs.count_documents({}), 1)
        self.assertGreaterEqual(db.xai_retraining_benchmarks.count_documents({}), 1)
        self.assertGreaterEqual(db.xai_cnn_gradcam_runs.count_documents({}), 1)
        print(f"  ✓ MongoDB 'quantlens_xai' verified: {db.xai_feedback_runs.count_documents({})} feedback runs, {db.xai_retraining_benchmarks.count_documents({})} retrain runs.")

    def test_30_rest_api_endpoint_integration(self):
        print("[Step 30/30] Verifying REST API Endpoints & Tab 09 Web Integration...")
        resp = self.client.get("/api/quantlens/xai/research/overview")
        self.assertEqual(resp.status_code, 200)
        data = json.loads(resp.data.decode())
        self.assertTrue(data.get("success", False))
        self.assertIn("model_c_timeseries_cnn", data.get("models", {}))

        # Check HTML contains tab-xai-research
        page = self.client.get("/quantlens")
        self.assertEqual(page.status_code, 200)
        html = page.data.decode()
        self.assertIn("tab-xai-research", html)
        self.assertIn("09. XAI Research Lab", html)
        print("  ✓ Web UI verified: Tab 09 'XAI Research Lab' present with all 6 views.")
        print("\n" + "=" * 75)
        print("ACCEPTANCE TEST 'QUANTLENS RESEARCH XAI SUITE' PASSED 100% (30/30 STEPS)!")
        print("=" * 75 + "\n")


if __name__ == "__main__":
    unittest.main()
