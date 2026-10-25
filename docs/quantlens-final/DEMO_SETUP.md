# QuantLens-XAI: Faculty Demonstration Setup & Pre-Flight Checklist

**Course:** Explainable Artificial Intelligence (BCSE418L)  
**Academic Year:** 2026–27  
**Student:** Nikhil Anand  
**Target Audience:** Course Professor & Evaluation Panel

---

## 1. 5-Minute Pre-Flight Checklist

Before entering the faculty demonstration or viva room, complete these four checks:

### Check 1: Start Ollama Daemon
```bash
ollama serve &
```
Verify the model responds:
```bash
curl -s http://127.0.0.1:11434/api/tags
# Expected: {"models":[{"name":"qwen2.5:0.5b", ...}]}
```

### Check 2: Launch the QuantLens Platform
```bash
./start_quantlens.sh
```
Or:
```bash
python3 app.py
```

### Check 3: Reset the Paper Trading Account
```bash
./reset_quantlens_demo.sh
```
This resets the virtual cash balance to a pristine ₹1,00,000.00 INR and clears previous temporary simulation orders.

### Check 4: Open Browser
Navigate to:
```
http://127.0.0.1:5001/quantlens
```
Confirm the top academic banner displays:
`⚠️ PAPER TRADING — VIRTUAL FUNDS ONLY • Strictly Educational & Research Environment (BCSE418L)`
and the Ollama status pill glows green (`Ollama: qwen2.5:0.5b (Metal GPU)`).

---

## 2. Emergency Backup Procedures

- **If Ollama crashes during the presentation**:
  The platform includes an automated deterministic fallback parser. The UI will continue operating smoothly and informatively without throwing 500 errors.
- **If port 5001 is already in use**:
  The application automatically checks port 5000 and 5001. Simply access `http://127.0.0.1:5000/quantlens` or specify `PORT=5002 python3 app.py`.
- **If offline without Wi-Fi**:
  All historical daily datasets (`RELIANCE.NS.csv`, `TCS.NS.csv`, `INFY.NS.csv`, `NIFTY50.csv`) and model weights are cached locally on disk. The application operates with 100% functionality without any internet connection.
