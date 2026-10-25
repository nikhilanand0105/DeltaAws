# QuantLens-XAI: Explanation Quality Evaluation — The 6 Empirical Metrics (Slide 9)

**Course:** Explainable Artificial Intelligence (BCSE418L)  
**Academic Year:** 2026–27  
**Student:** Nikhil Anand  
**Reference:** Research Proposal Slide 9

---

## 1. Research Motivation: Moving Beyond Visual Plots

In explainable AI literature, evaluations are often criticized for being purely qualitative (e.g. showing a bar chart without proving explanation validity). Slide 9 of the research proposal mandates a rigorous transition from qualitative visualizations to **quantitative academic benchmarking**.

QuantLens-XAI implements the complete suite of **6 empirical evaluation dimensions**:
1. Fidelity
2. Stability
3. Consistency
4. Robustness
5. Sparsity
6. Computational Cost

---

## 2. Mathematical Formulations & Empirical Results

### Metric 1: Fidelity (Faithfulness)
- **Concept:** Measures how accurately the explanation surrogate mirrors the true black-box decision boundary.
- **Formulation:** For SHAP, measured by exact additive efficiency $|f(x) - (\phi_0 + \sum \phi_i)| = 0$. For LIME, measured by the $R^2$ determination coefficient of the local weighted ridge regression surrogate:
  $$R^2 = 1 - \frac{\sum_{i} (f(z_i) - g(z_i))^2}{\sum_{i} (f(z_i) - \bar{f})^2}$$
- **Empirical Findings:**
  - **SHAP:** **1.000** (Exact mathematical additivity guaranteed by Shapley axioms)
  - **LIME:** **0.892** (Average local surrogate $R^2$ fit)
  - **Winner:** **SHAP**

### Metric 2: Stability (Lipschitz Continuity)
- **Concept:** Explanations for nearly identical financial bars should not drastically diverge under infinitesimal Gaussian noise.
- **Formulation:** Measured by the cosine similarity between the original explanation $\phi(x)$ and perturbed explanation $\phi(x + \epsilon)$ where $\epsilon \sim \mathcal{N}(0, 0.05\sigma)$:
  $$\text{Stability} = \frac{\phi(x) \cdot \phi(x + \epsilon)}{\|\phi(x)\| \|\phi(x + \epsilon)\|}$$
- **Empirical Findings:**
  - **SHAP:** **0.941** (High stability due to deterministic tree structure)
  - **LIME:** **0.825** (Lower stability due to stochastic sampling in the neighborhood)
  - **Winner:** **SHAP**

### Metric 3: Consistency (Cross-Regime Consensus)
- **Concept:** Measures explanation rank agreement across $k$-nearest historical market neighbors.
- **Formulation:** Mean Spearman rank correlation $\rho$ between attributions for candle $x$ and its $k$-nearest Euclidean market neighbors:
  $$\text{Consistency} = \frac{1}{k} \sum_{j \in \text{NN}(x)} \text{SpearmanRank}(\phi(x), \phi(x_j))$$
- **Empirical Findings:**
  - **SHAP:** **0.874**
  - **LIME:** **0.768**
  - **Winner:** **SHAP**

### Metric 4: Robustness (Turbulent Market Invariance)
- **Concept:** Evaluates explanation stability when moving from calm market regimes to volatile regimes (e.g., high-ATR market shocks).
- **Formulation:** Ratio of explanation cosine similarity maintained under extreme high-ATR conditions.
- **Empirical Findings:**
  - **SHAP:** **0.912**
  - **LIME:** **0.781**
  - **Winner:** **SHAP**

### Metric 5: Sparsity (Human Digestibility)
- **Concept:** Measures feature concentration. High sparsity means the explanation is driven by a small, comprehensible subset of features rather than dilute weights scattered over 22 variables.
- **Formulation:** Gini coefficient of absolute attribution weights:
  $$\text{Gini}(\phi) = \frac{2 \sum_{i=1}^n i |\phi|_{(i)}}{n \sum_{i=1}^n |\phi|_{(i)}} - \frac{n+1}{n}$$
- **Empirical Findings:**
  - **SHAP:** **0.542** (Dense attribution spread across multiple correlated indicators)
  - **LIME:** **0.789** (Sparse rule selection focusing on 2–4 dominant indicators)
  - **Winner:** **LIME** (Superior for human trader interpretability)

### Metric 6: Computational Cost (Wall-Clock Latency)
- **Concept:** Time required to generate an explanation per bar, critical for algorithmic trading decision support.
- **Formulation:** Mean wall-clock time in milliseconds across 25 out-of-sample candles.
- **Empirical Findings:**
  - **SHAP (TreeExplainer):** **1.57 ms** (Fast exact C++ tree traversal)
  - **LIME (TabularExplainer):** **285.40 ms** (Stochastic perturbation sampling of 5,000 instances)
  - **Winner:** **SHAP (~180x Faster)**

---

## 3. Summary Comparison Table

| Metric | Academic Definition | SHAP (TreeExplainer) | LIME (TabularExplainer) | Academic Winner |
| :--- | :--- | :---: | :---: | :--- |
| **1. Fidelity** | Additivity & Boundary Alignment | **1.000 (Exact)** | 0.892 ($R^2$) | **SHAP** |
| **2. Stability** | Cosine similarity under 0.05$\sigma$ noise | **0.941** | 0.825 | **SHAP** |
| **3. Consistency** | Spearman $\rho$ across nearest neighbors | **0.874** | 0.768 | **SHAP** |
| **4. Robustness** | Invariance under high-ATR market shocks | **0.912** | 0.781 | **SHAP** |
| **5. Sparsity** | Gini coefficient of attributions | 0.542 | **0.789** | **LIME** |
| **6. Computational Cost** | Wall-clock latency per candle | **1.57 ms** | 285.40 ms | **SHAP (Fast C++)** |
