# QuantLens-XAI: Machine Learning and Deep Learning Models

## 1. Dual Model Architecture
QuantLens-XAI deploys two complementary predictive architectures:
1. **Gradient Boosted Decision Trees (XGBoost)**: Optimized for tabular technical feature interaction and lightning-fast CPU inference.
2. **Deep Multilayer Perceptron (PyTorch)**: Implemented with Apple Silicon Metal Performance Shaders (MPS / CPU fallback) for non-linear representation learning.

---

## 2. Model Specifications & Feature Inputs
Input features ($d=10$):
- Normalized close-to-open ratio
- EMA 10 to EMA 30 ratio
- RSI (14) normalized $[0, 1]$
- MACD histogram normalized
- Volume momentum (5-day rolling)
- ATR percentage volatility
- 5-day historical return
- 20-day historical return
- High-to-low daily spread
- Bollinger %B indicator

### XGBoost Model (`models/xgboost_reliance.json`)
- Max Depth: 4
- Learning Rate: 0.05
- Estimators: 100
- Objective: `binary:logistic`

### PyTorch MLP (`models/pytorch_reliance.pt`)
- Input Layer: 10 units
- Hidden Layer 1: 32 units (ReLU, Dropout 0.2)
- Hidden Layer 2: 16 units (ReLU)
- Output Layer: 1 unit (Sigmoid probability)
