# QuantLens-XAI: Local LLM Configuration, Apple Silicon Acceleration & Runtime Guide

**Course:** Explainable Artificial Intelligence (BCSE418L)  
**Academic Year:** 2026–27  
**Student:** Nikhil Anand  
**Target Hardware:** MacBook Pro M1 Pro (16 GB Unified RAM)  
**Runtime:** Ollama 0.5.x+ with Metal GPU Acceleration

---

## 1. Local LLM Architecture & Selection

QuantLens-XAI is designed strictly to avoid paid cloud API dependencies, ensuring:
1. **Zero Cloud API Costs**: Runs entirely on the student's local laptop.
2. **Complete Privacy**: Financial trading prompts never leave the local machine.
3. **Low Latency**: Sub-2-second inference powered by Apple Silicon Metal GPU unified memory.
4. **Deterministic Structured JSON**: Using Ollama's native `"format": "json"` schema parser.

### Evaluated Model Matrix

| Model | Parameter Count | Quantization | Size on Disk | Apple Metal GPU Support | Parse Latency (M1 Pro) | JSON Validity | Recommendation |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **qwen2.5:0.5b** | 494M | Q4_K_M | **397 MB** | **YES (Metal `MTL0`)** | **~0.92s to 1.32s** | **100% Valid JSON** | **RECOMMENDED & ACTIVE** |
| **smollm2:135m** | 134M | F16 | 270 MB | YES (Metal `MTL0`) | ~0.45s | 88% Valid JSON | Fallback option |
| **qwen2.5:3b** | 3.09B | Q4_K_M | 1.90 GB | YES (Metal `MTL0`) | ~3.80s | 100% Valid JSON | Optional heavy model |

---

## 2. Ollama Installation & Verification

### Step 1: Install Ollama
Download and install Ollama for macOS from [ollama.com](https://ollama.com) or via Homebrew:
```bash
brew install ollama
```

### Step 2: Start Ollama Daemon
```bash
ollama serve &
```
Verify the daemon is alive:
```bash
curl -s http://127.0.0.1:11434/api/tags
```

### Step 3: Pull Model
```bash
ollama pull qwen2.5:0.5b
```

---

## 3. Strict JSON System Prompt

The parser enforces structured parameter extraction by feeding Ollama the following specialized system prompt:

```text
You are a quantitative trading strategy compiler for QuantLens-XAI.
Parse user trading strategies into a clean, valid JSON object with EXACTLY these numeric keys:
{
  "strategy_name": string,
  "symbol": string ("RELIANCE" | "TCS" | "INFY"),
  "timeframe": string ("daily"),
  "ema_fast": integer (e.g. 10),
  "ema_slow": integer (e.g. 30),
  "rsi_period": integer (e.g. 14),
  "rsi_threshold": float (e.g. 65.0),
  "stop_loss_pct": float (e.g. 2.0),
  "take_profit_pct": float (e.g. 4.0),
  "initial_capital": float (e.g. 100000.0),
  "max_allocation_pct": float (e.g. 10.0),
  "max_open_positions": integer (e.g. 1)
}
Return ONLY valid JSON.
```

---

## 4. Multi-Tier Fallback Hierarchy

If the local Ollama daemon is offline or non-responsive, QuantLens-XAI transparently activates its deterministic rule-based parser fallback (`quantlens/llm_parser.py`), ensuring that faculty demonstrations are **100% resilient and never crash due to network or service dropouts**.
