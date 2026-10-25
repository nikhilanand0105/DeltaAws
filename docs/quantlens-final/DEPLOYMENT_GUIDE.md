# QuantLens-XAI: Local Deployment & Operations Guide

## 1. Prerequisites
- **Operating System**: macOS (Apple Silicon recommended)
- **Python**: Python 3.9+ with pip
- **Database**: MongoDB Community Edition 7.0+
- **Local LLM Engine**: Ollama (`ollama serve`)

---

## 2. Installation Steps

### 1. Start MongoDB
```bash
brew services start mongodb-community@7.0
# Or direct command:
mongod --config /opt/homebrew/etc/mongod.conf --fork
```

### 2. Start Local Ollama Daemon & Pull Model
```bash
ollama serve &
ollama pull qwen2.5:0.5b
```

### 3. Install Python Dependencies
```bash
python3 -m pip install -r requirements.txt
python3 -m pip install pymongo python-docx reportlab selenium webdriver-manager
```

### 4. Execute JSON to MongoDB Migration (Idempotent)
```bash
python3 scripts/migrate_json_to_mongodb.py
```

### 5. Launch Application
```bash
./start_quantlens.sh
```
Access the application at `http://127.0.0.1:5001/quantlens`.

---

## 3. Automated System Verification
Run the 30-step test suite:
```bash
python3 -m unittest tests/test_quantlens_complete_demo.py
```
Ensure all 30 steps pass in $<5\text{ seconds}$.
