# QuantLens-XAI: Explainable AI Methodologies — SHAP & LIME Mathematical Foundations

**Course:** Explainable Artificial Intelligence (BCSE418L)  
**Academic Year:** 2026–27  
**Student:** Nikhil Anand  
**Reference:** Research Proposal Slide 8

---

## 1. Research Overview

In quantitative trading, machine learning models like Gradient Boosted Trees and Deep Neural Networks are traditionally treated as "black boxes": they produce a predicted probability for a price move without indicating *why* that prediction was made.

QuantLens-XAI implements two foundational and contrasting local attribution methodologies:
1. **SHAP (SHapley Additive exPlanations)** via `TreeExplainer`: Based on cooperative game theory, calculating exact Shapley values.
2. **LIME (Local Interpretable Model-agnostic Explanations)** via `LimeTabularExplainer`: Based on local perturbation and sparse linear surrogate models.

---

## 2. SHAP (TreeExplainer) Formulation

SHAP attributes the deviation of a model's prediction $f(x)$ from the expected base value $E[f(x)]$ across the input features:

$$f(x) = \phi_0 + \sum_{i=1}^{M} \phi_i(x)$$

Where the Shapley value $\phi_i$ for feature $i$ is uniquely defined by:

$$\phi_i(f, x) = \sum_{S \subseteq F \setminus \{i\}} \frac{|S|! (|F| - |S| - 1)!}{|F|!} \left[ f_x(S \cup \{i\}) - f_x(S) \right]$$

### TreeExplainer Advantages in Finance
- **Exact Additivity**: The sum of feature attributions plus the expected value exactly equals the model output log-odds or probability.
- **Computational Efficiency**: `TreeExplainer` traverses all decision paths of the 120 trees in XGBoost in polynomial time $O(T L D^2)$, executing in **under 2 milliseconds** per candle.
- **Key Financial Attributions**: Typically identifies `price_to_ema30`, `rsi_14`, and `macd_hist` as the primary drivers of directional BUY/SELL transitions.

---

## 3. LIME (LimeTabularExplainer) Formulation

LIME approximates the complex global model $f$ locally around a specific candle $x$ using an interpretable linear surrogate model $g \in G$:

$$\xi(x) = \arg\min_{g \in G} \mathcal{L}(f, g, \pi_x) + \Omega(g)$$

Where:
- $\pi_x(z) = \exp\left(-\frac{D(x, z)^2}{\sigma^2}\right)$ is an exponential kernel defining the local neighborhood around candle $x$.
- $\mathcal{L}$ is the squared loss of surrogate $g$ approximating $f$ on perturbed samples $z$.
- $\Omega(g)$ penalizes model complexity to enforce sparsity (e.g., limiting explanations to $K$ dominant rules).

### LIME Output Format
Rather than continuous attribution values alone, LIME produces bounded decision rules that are directly interpretable to financial analysts:
- Example: `-0.27 < rsi_14 <= 0.49` (Weight: $-0.0315$, Bearish Resistance)
- Example: `price_to_ema30 > 0.012` (Weight: $+0.0480$, Bullish Support)

---

## 4. Cross-Explainer Consensus & Correlation

QuantLens-XAI computes the **Spearman Rank Correlation ($\rho$)** between SHAP and LIME feature attribution vectors for every historical candle:

$$\rho = 1 - \frac{6 \sum d_i^2}{n(n^2 - 1)}$$

Where $d_i$ is the difference between the ranks assigned to feature $i$ by SHAP versus LIME.
- **Observed Regime Behavior**:
  - In strong trending regimes, both SHAP and LIME agree strongly on moving average ratios ($\rho > 0.70$).
  - In transitional/volatile regimes, LIME's perturbation sampling introduces surrogate variance, leading to lower rank agreement ($\rho \approx 0.30 - 0.45$). This discrepancy is a primary research finding of QuantLens-XAI.
