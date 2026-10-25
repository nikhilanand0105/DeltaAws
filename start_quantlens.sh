#!/usr/bin/env bash
# QuantLens-XAI: Automated Startup Script for macOS (Apple Silicon M1 Pro)
# Launches Ollama background daemon (if needed), checks MongoDB 7.0 daemon,
# verifies ML models, and starts the Flask application on port 5001.

set -e

echo "======================================================================"
echo "    QuantLens-XAI: Explainable Algorithmic Trading Platform"
echo "    BCSE418L Academic Year 2026-27 | Student: Nikhil Anand"
echo "    Architecture: Hybrid SQLite 3 + MongoDB Community Edition 7.0"
echo "======================================================================"

# 1. Check MongoDB Community 7.0
echo "[1/4] Checking MongoDB daemon on port 27017..."
if nc -z 127.0.0.1 27017 2>/dev/null; then
    echo "  ✓ MongoDB Community 7.0 is active and accepting connections on port 27017."
else
    echo "  Starting MongoDB daemon..."
    brew services start mongodb-community@7.0 || mongod --config /opt/homebrew/etc/mongod.conf --fork
    sleep 2
    if nc -z 127.0.0.1 27017 2>/dev/null; then
        echo "  ✓ MongoDB started successfully."
    else
        echo "  ⚠️ Warning: MongoDB could not be reached. Ensure mongod is running."
    fi
fi

# 2. Check Ollama
echo "[2/4] Checking local Ollama runtime..."
if curl -s http://127.0.0.1:11434/api/tags > /dev/null; then
    echo "  ✓ Ollama daemon is active on port 11434."
else
    echo "  Starting Ollama daemon in background..."
    ollama serve > /dev/null 2>&1 &
    sleep 2
    if curl -s http://127.0.0.1:11434/api/tags > /dev/null; then
        echo "  ✓ Ollama daemon started successfully."
    else
        echo "  ⚠️ Warning: Ollama could not be started automatically. Fallback parser will be active."
    fi
fi

# 3. Check Models
echo "[3/4] Verifying model artifacts..."
if [ -f "models/xgboost_reliance.json" ] && [ -f "models/pytorch_mlp_reliance.pt" ]; then
    echo "  ✓ XGBoost and PyTorch MLP models verified."
else
    echo "  ⚠️ Training models..."
    python3 -c "from quantlens.ml_models import ModelManager; m = ModelManager('RELIANCE'); m.train_models()"
fi

# 4. Start Flask Web Application
PORT=${PORT:-5001}
echo "[4/4] Starting QuantLens web application on http://127.0.0.1:${PORT}/quantlens ..."
echo ""
echo "Access QuantLens-XAI in your browser at:"
echo "👉 http://127.0.0.1:${PORT}/quantlens"
echo ""

PORT=${PORT} python3 app.py
