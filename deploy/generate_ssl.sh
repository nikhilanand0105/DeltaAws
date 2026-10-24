#!/usr/bin/env bash
# Generates self-signed TLS certificates for immediate HTTPS functionality on EC2
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"
CERTS_DIR="$PROJECT_ROOT/nginx/certs"

mkdir -p "$CERTS_DIR"

if [[ -f "$CERTS_DIR/cert.pem" && -f "$CERTS_DIR/key.pem" ]]; then
    echo "[INFO] SSL certificates already exist in $CERTS_DIR. Skipping generation."
    exit 0
fi

echo "[INFO] Generating self-signed TLS certificate for EC2 deployment..."
openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout "$CERTS_DIR/key.pem" \
    -out "$CERTS_DIR/cert.pem" \
    -subj "/C=US/ST=Cloud/L=Virtual/O=BCSE355L-DA3/OU=TradingSystem/CN=delta-bot.local"

chmod 600 "$CERTS_DIR/key.pem"
chmod 644 "$CERTS_DIR/cert.pem"

echo "[SUCCESS] Self-signed certificates generated successfully in $CERTS_DIR"
