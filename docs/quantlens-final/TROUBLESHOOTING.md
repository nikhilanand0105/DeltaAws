# QuantLens-XAI: Operational Troubleshooting Guide

## 1. Common Issues & Resolutions

### Issue 1: MongoDB Connection Refused (`localhost:27017`)
- **Symptoms**: Error logs reporting `ServerSelectionTimeoutError` when accessing paper broker or XAI tab.
- **Resolution**:
  ```bash
  brew services restart mongodb-community@7.0
  # Verify port listening:
  nc -zv 127.0.0.1 27017
  ```

### Issue 2: Ollama LLM Timeout or Connection Error (`localhost:11434`)
- **Symptoms**: Strategy parsing displays "Fallback Regex Parser" badge with latency $<50\text{ ms}$.
- **Resolution**:
  ```bash
  ollama serve &
  ollama list  # ensure qwen2.5:0.5b is listed
  ```

### Issue 3: Port 5001 Already in Use
- **Symptoms**: `OSError: [Errno 48] Address already in use`
- **Resolution**:
  ```bash
  lsof -ti:5001 | xargs kill -9
  ./start_quantlens.sh
  ```

### Issue 4: Resetting All Demo Data
- **Symptoms**: Inconsistent paper broker capital or corrupt state during presentation.
- **Resolution**:
  ```bash
  ./reset_quantlens_demo.sh
  ```
  This resets the paper broker in MongoDB to initial capital of ₹10,00,000 and clears orphaned positions.
