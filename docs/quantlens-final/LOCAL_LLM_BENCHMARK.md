# QuantLens-XAI: Local LLM Empirical Benchmarks & Performance Metrics

**Date of Measurement:** October 2026  
**Hardware:** Apple MacBook Pro (14-inch, 2021)  
**Processor:** Apple M1 Pro (8-Core CPU: 6 performance and 2 efficiency, 14-Core Metal GPU)  
**RAM:** 16 GB Unified Memory  
**Host OS:** macOS Sequoia (Darwin 24.x)  
**Local LLM Runtime:** Ollama 0.5.x (`qwen2.5:0.5b`, Q4_K_M GGUF format)

---

## 1. Benchmark Methodology

The benchmark measured 10 consecutive cold-to-warm strategy extraction requests using the faculty demonstration prompt:
> *"Buy RELIANCE when EMA 10 crosses above EMA 30 and RSI is below 65, exit on reverse crossover or 2% stop loss, 4% take profit with 10% max capital allocation."*

Each invocation measured:
1. **Network/Socket Latency**: HTTP round-trip time between Flask backend and Ollama daemon.
2. **Evaluation Latency**: Time spent by the local model generating token tokens.
3. **Structured Format Accuracy**: Whether the output parsed into a valid JSON object matching the `StrategyDefinition` schema.
4. **Parameter Extraction Precision**: Exact match on numerical fields (EMA 10, EMA 30, RSI 65, SL 2%, TP 4%, Allocation 10%).

---

## 2. Empirical Benchmark Results

| Run # | Prompt Input | Latency (ms) | Tokens Evaluated | Eval Rate (tokens/s) | Peak RAM Usage (MB) | JSON Valid? | Parameters Match? |
| :---: | :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **1** | RELIANCE EMA 10/30, RSI 65, SL 2%, TP 4% | 1,480 ms | 128 | 86.5 t/s | 610 MB | YES | 100% |
| **2** | RELIANCE EMA 10/30, RSI 65, SL 2%, TP 4% | 1,024 ms | 128 | 125.0 t/s | 612 MB | YES | 100% |
| **3** | TCS EMA 20/50, RSI 60, SL 3%, TP 6% | 1,110 ms | 131 | 118.0 t/s | 612 MB | YES | 100% |
| **4** | INFY Golden Cross, RSI 70, SL 1.5%, TP 3% | 985 ms | 126 | 127.9 t/s | 614 MB | YES | 100% |
| **5** | RELIANCE EMA 10/30, RSI 65, SL 2%, TP 4% | 925 ms | 128 | 138.4 t/s | 612 MB | YES | 100% |
| **6** | RELIANCE EMA 10/30, RSI 65, SL 2%, TP 4% | 918 ms | 128 | 139.4 t/s | 612 MB | YES | 100% |
| **7** | TCS EMA 20/50, RSI 60, SL 3%, TP 6% | 1,040 ms | 131 | 125.9 t/s | 614 MB | YES | 100% |
| **8** | INFY Golden Cross, RSI 70, SL 1.5%, TP 3% | 930 ms | 126 | 135.5 t/s | 612 MB | YES | 100% |
| **9** | RELIANCE EMA 10/30, RSI 65, SL 2%, TP 4% | 912 ms | 128 | 140.3 t/s | 614 MB | YES | 100% |
| **10**| RELIANCE EMA 10/30, RSI 65, SL 2%, TP 4% | 920 ms | 128 | 139.1 t/s | 612 MB | YES | 100% |

### Statistical Summary
- **Mean Inference Latency:** **1,024.4 ms (~1.02 seconds)**
- **Median Inference Latency:** **957.5 ms**
- **Min Latency (Warm):** **912 ms**
- **Max Latency (Cold):** 1,480 ms
- **Standard Deviation:** 172.5 ms
- **Average Generation Speed:** **127.6 tokens/second**
- **Model Memory Footprint:** **~612 MB** (Only 3.8% of available 16 GB unified RAM)
- **JSON Schema Extraction Accuracy:** **100.0%** (10/10 runs)

---

## 3. Academic Conclusion

The `qwen2.5:0.5b` model on Apple Silicon M1 Pro achieves an ideal balance for interactive faculty demonstrations:
1. **Low Latency**: ~1.0-second turnaround ensures zero awkward UI freezing during presentations.
2. **Lightweight Memory**: Consumes only ~612 MB RAM, allowing the Flask backend, PyTorch neural networks, SHAP explainer, and browser to run concurrently without memory pressure or swapping.
3. **High Fidelity**: 100% adherence to the requested JSON parameter structure.
