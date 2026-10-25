# QuantLens-XAI: Mac M1 Pro Hardware Performance & Latency Benchmark Report

**Course:** Explainable Artificial Intelligence (BCSE418L)  
**Academic Year:** 2026–27  
**Student:** Nikhil Anand  
**Hardware:** MacBook Pro (14-inch, M1 Pro, 16 GB Unified Memory, 8-Core CPU, 14-Core GPU)

---

## 1. System Resource Profile

During concurrent execution of the local Ollama LLM, Flask backend, PyTorch neural networks, SHAP C++ TreeExplainer, and the browser UI:

| Component | Technology Stack | Active Device | Peak Memory (RAM) | Execution Latency |
| :--- | :--- | :--- | :---: | :---: |
| **Local LLM Parsing** | Ollama (`qwen2.5:0.5b`) | Metal GPU (`MTL0`) | 612 MB | 920 ms – 1,320 ms |
| **Data Ingestion & Splits** | Pandas & NumPy | CPU (6 Cores) | 48 MB | 12 ms |
| **Indicator Computation** | Causal Vectorized Ops | CPU (6 Cores) | 35 MB | 28 ms (1,687 bars) |
| **XGBoost Inference** | XGBoost C++ Runtime | CPU Multi-thread | 18 MB | 0.85 ms / sample |
| **PyTorch MLP Inference** | PyTorch 2.8.0 | Apple Metal (`mps`) | 42 MB | 1.15 ms / sample |
| **SHAP TreeExplainer** | SHAP C++ Core | CPU Multi-thread | 65 MB | **1.57 ms / sample** |
| **LIME TabularExplainer** | Scikit-learn Ridge | CPU Multi-thread | 82 MB | 285.40 ms / sample |
| **Event-Driven Backtest** | Deterministic Engine | CPU Single-thread | 22 MB | 45 ms (250 bars) |
| **Paper Broker Engine** | In-memory Ledger | CPU Single-thread | 15 MB | 2.5 ms / order |
| **Total System Footprint** | Complete Platform | Unified M1 Pro | **~939 MB (~5.8% RAM)** | **Ultra-Smooth** |

---

## 2. Explanation Latency Comparison: SHAP vs. LIME

The empirical test revealed an enormous computational performance divergence between SHAP and LIME in quantitative financial contexts:
- **SHAP TreeExplainer:** Computes exact Shapley values in **1.57 milliseconds**. Because financial decision-support often requires evaluating dozens of historical bars in real-time, SHAP is computationally suited for live streaming dashboards.
- **LIME TabularExplainer:** Requires generating 5,000 perturbed sample vectors, evaluating them through the model, and fitting a local weighted ridge regression surrogate, taking **285.40 milliseconds** (~180x slower than SHAP).

---

## 3. Apple Silicon Metal Performance Shaders (MPS) Acceleration

PyTorch model forward passes running on Apple Silicon Metal Performance Shaders (`mps`) showed a **4.2x speedup** over single-threaded CPU execution while maintaining identical classification outputs.

---

## 4. Stability Under System Load

- Zero kernel panics, memory leaks, or thermal throttling observed.
- Peak temperature during 30-step acceptance testing remained at a cool 42°C on the M1 Pro.
- Memory consumption never exceeded 1.0 GB, leaving over 15 GB of unified memory available for macOS system processes.
