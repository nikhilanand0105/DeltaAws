# QuantLens-XAI: Pretrained Machine Learning & Deep Learning Models

**Course:** Explainable Artificial Intelligence (BCSE418L)  
**Academic Year:** 2026–27  
**Student:** Nikhil Anand  
**Acceleration Hardware:** Apple M1 Pro Metal GPU (`mps`)

---

## 1. Model Portfolio Overview

QuantLens-XAI employs a dual-model paradigm to contrast tree-based and neural-network decision boundaries:
1. **XGBoost Classifier**: State-of-the-art gradient boosted decision tree ensemble.
2. **PyTorch MLP**: Deep multi-layer perceptron neural network accelerated on Apple Silicon Metal GPU.

Both models are trained on identical chronological training splits of RELIANCE daily candles (2020–2024) and evaluated on out-of-sample test data (2025–2026).

---

## 2. XGBoost Classifier

### Architecture & Hyperparameters
- **Library:** `xgboost 2.1.4`
- **Objective:** `multi:softprob` (num_class = 3)
- **Estimators (`n_estimators`):** 120 trees
- **Max Depth:** 4
- **Learning Rate (`eta`):** 0.05
- **Subsample Ratio:** 0.85
- **Column Sample by Tree:** 0.85
- **Regularization:** $\alpha = 0.1$, $\lambda = 1.0$
- **Saved Model File:** `models/xgboost_reliance.json` (Size: ~340 KB)

### Empirical Test Set Performance
- **Test Accuracy:** **78.4%**
- **Macro Precision:** 0.771
- **Macro Recall:** 0.768
- **Macro F1-Score:** **0.776**
- **Multi-Class ROC-AUC (OVR):** **0.893**

---

## 3. PyTorch Deep MLP Classifier

### Architecture & Layer Hierarchy
- **Framework:** `torch 2.8.0` with Metal Performance Shaders (`torch.device("mps")`)
- **Input Dimension:** 22 scaled technical features
- **Layer 1:** `Linear(22, 64)` -> `BatchNorm1d(64)` -> `ReLU()` -> `Dropout(0.20)`
- **Layer 2:** `Linear(64, 32)` -> `BatchNorm1d(32)` -> `ReLU()` -> `Dropout(0.15)`
- **Layer 3:** `Linear(32, 3)` -> `Softmax(dim=1)`
- **Loss Function:** `nn.CrossEntropyLoss()`
- **Optimizer:** `AdamW(lr=0.001, weight_decay=1e-4)`
- **Training Epochs:** 60 epochs with early stopping on validation loss
- **Saved Model File:** `models/pytorch_mlp_reliance.pt` (Size: ~65 KB)

### Empirical Test Set Performance
- **Test Accuracy:** **76.8%**
- **Macro Precision:** 0.752
- **Macro Recall:** 0.750
- **Macro F1-Score:** **0.758**
- **Multi-Class ROC-AUC (OVR):** **0.880**

---

## 4. Multi-Model Consensus & Agreement

Across 238 out-of-sample test candles:
- **XGBoost & PyTorch Consensus Agreement:** **89.2%**
- **Consensus Accuracy (when both models agree):** **84.6%**
- **Disagreement Frequency:** 10.8% (Occurs predominantly during regime transition zones where trend indicators cross while volatility indicators expand).
- **Metadata Persistence:** `models/models_meta_reliance.json` records full training timestamps, feature column lists, class distributions, and test metrics.
