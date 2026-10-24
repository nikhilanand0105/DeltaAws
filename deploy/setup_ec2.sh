#!/usr/bin/env bash
# ==============================================================================
# EC2 Bootstrap Script for Delta Algorithmic Trading Bot
# Compatible with Amazon Linux 2023 and Ubuntu 22.04 / 24.04 LTS
# ==============================================================================
set -euo pipefail

echo "=========================================================="
echo " Starting Delta Trading Bot AWS EC2 Deployment Setup..."
echo " Timestamp: $(date -u +"%Y-%m-%dT%H:%M:%SZ")"
echo "=========================================================="

APP_DIR="/opt/delta-bot"

# 1. Detect Operating System
if [ -f /etc/os-release ]; then
    . /etc/os-release
    OS=$ID
else
    echo "[ERROR] Cannot determine OS distribution."
    exit 1
fi

echo "[INFO] Detected OS: $OS"

# 2. Configure 2.0 GiB Swap File to Prevent Out-Of-Memory on 1 GiB Instances
if [ ! -f /swapfile ]; then
    echo "[INFO] Configuring 2.0 GiB swapfile on EBS volume for memory stability..."
    dd if=/dev/zero of=/swapfile bs=1M count=2048 status=progress
    chmod 600 /swapfile
    mkswap /swapfile
    swapon /swapfile
    if ! grep -q '/swapfile' /etc/fstab; then
        echo '/swapfile none swap sw 0 0' >> /etc/fstab
    fi
    echo "[SUCCESS] Swapfile configured. Total system memory now ~3.0 GiB."
fi

# 3. Install Packages & Docker
if [[ "$OS" == "amzn" ]]; then
    echo "[INFO] Updating Amazon Linux packages..."
    dnf update -y
    dnf install -y --allowerasing docker git openssl jq amazon-cloudwatch-agent python3-pip

    # Install Certbot via pip for automated browser-trusted Let's Encrypt SSL
    pip3 install --no-cache-dir certbot || true

    # Install Docker Compose Plugin
    mkdir -p /usr/local/lib/docker/cli-plugins
    curl -SL "https://github.com/docker/compose/releases/latest/download/docker-compose-linux-$(uname -m)" -o /usr/local/lib/docker/cli-plugins/docker-compose
    chmod +x /usr/local/lib/docker/cli-plugins/docker-compose
    ln -sf /usr/local/lib/docker/cli-plugins/docker-compose /usr/bin/docker-compose

    systemctl enable docker.service
    systemctl start docker.service
    usermod -aG docker ec2-user || true

elif [[ "$OS" == "ubuntu" || "$OS" == "debian" ]]; then
    echo "[INFO] Updating Ubuntu packages..."
    apt-get update -y
    apt-get install -y ca-certificates curl gnupg lsb-release git openssl jq certbot

    # Install official Docker
    mkdir -p /etc/apt/keyrings
    curl -fsSL https://download.docker.com/linux/ubuntu/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg --yes
    echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | tee /etc/apt/sources.list.d/docker.list > /dev/null
    apt-get update -y
    apt-get install -y docker-ce docker-ce-cli containerd.io docker-compose-plugin

    # Install CloudWatch Agent
    ARCH=$(dpkg --print-architecture)
    curl -SL "https://amazoncloudwatch-agent.s3.amazonaws.com/ubuntu/$ARCH/latest/amazon-cloudwatch-agent.deb" -o /tmp/amazon-cloudwatch-agent.deb
    dpkg -i -E /tmp/amazon-cloudwatch-agent.deb
    rm -f /tmp/amazon-cloudwatch-agent.deb

    systemctl enable docker.service
    systemctl start docker.service
    usermod -aG docker ubuntu || true
fi

# 4. Create Deployment Directory
echo "[INFO] Setting up application directory in $APP_DIR..."
mkdir -p "$APP_DIR"
cd "$APP_DIR"

# Ensure instance directory exists for SQLite database persistence
mkdir -p "$APP_DIR/instance"
chmod -R 777 "$APP_DIR/instance"

# 5. Acquire Browser-Trusted Let's Encrypt TLS Certificate via sslip.io
mkdir -p "$APP_DIR/nginx/certs"

# Fetch public IPv4
IMDS_TOKEN=$(curl -s -X PUT "http://169.254.169.254/latest/api/token" -H "X-aws-ec2-metadata-token-ttl-seconds: 60" || true)
if [ -n "$IMDS_TOKEN" ]; then
    PUBLIC_IP=$(curl -s -H "X-aws-ec2-metadata-token: $IMDS_TOKEN" http://169.254.169.254/latest/meta-data/public-ipv4 || true)
else
    PUBLIC_IP=$(curl -s http://169.254.169.254/latest/meta-data/public-ipv4 || curl -s https://api.ipify.org || true)
fi

SSL_DOMAIN=""
if [ -n "$PUBLIC_IP" ]; then
    # e.g. 13.234.56.78 -> 13-234-56-78.sslip.io (free wildcard DNS resolving to the IP)
    IP_DASH=${PUBLIC_IP//./-}
    SSL_DOMAIN="${IP_DASH}.sslip.io"
    echo "[INFO] Target Browser-Trusted Domain: $SSL_DOMAIN"

    # Stop any conflicting process on port 80 before certbot runs
    docker compose down 2>/dev/null || true

    echo "[INFO] Requesting browser-trusted Let's Encrypt certificate for $SSL_DOMAIN..."
    if command -v certbot >/dev/null 2>&1; then
        certbot certonly --standalone -d "$SSL_DOMAIN" \
            --agree-tos --register-unsafely-without-email \
            --non-interactive || echo "[WARN] Certbot automated issuance skipped or failed. Falling back to high-grade self-signed TLS."
    fi

    # If certbot succeeded, copy or link certs
    if [ -f "/etc/letsencrypt/live/$SSL_DOMAIN/fullchain.pem" ]; then
        echo "[SUCCESS] Browser-trusted certificate acquired from Let's Encrypt!"
        cp "/etc/letsencrypt/live/$SSL_DOMAIN/fullchain.pem" "$APP_DIR/nginx/certs/cert.pem"
        cp "/etc/letsencrypt/live/$SSL_DOMAIN/privkey.pem" "$APP_DIR/nginx/certs/key.pem"
    fi
fi

# Fallback: Generate self-signed certificate if Let's Encrypt cert is not available
if [[ ! -f "$APP_DIR/nginx/certs/cert.pem" || ! -f "$APP_DIR/nginx/certs/key.pem" ]]; then
    echo "[INFO] Generating 2048-bit self-signed SSL certificate fallback..."
    openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
        -keyout "$APP_DIR/nginx/certs/key.pem" \
        -out "$APP_DIR/nginx/certs/cert.pem" \
        -subj "/C=US/ST=Cloud/L=Virtual/O=BCSE355L-DA3/OU=TradingSystem/CN=${SSL_DOMAIN:-delta-bot.local}"
fi

chmod 600 "$APP_DIR/nginx/certs/key.pem"
chmod 644 "$APP_DIR/nginx/certs/cert.pem"

# 6. Create .env if missing (defaults to safe paper trading)
if [ ! -f "$APP_DIR/.env" ]; then
    echo "[INFO] Initializing default safe .env configuration..."
    cat <<'EOF' > "$APP_DIR/.env"
DELTA_API_KEY=MOCK_ALPHA_KEY_9847192847
DELTA_API_SECRET=MOCK_ALPHA_SECRET_1928374619
DELTA_BASE_URL=https://api.testnet.delta.exchange
PASSPHRASE=my_secure_trading_passphrase_123
DEFAULT_LEVERAGE=50
BALANCE_BUFFER_PCT=95
STRATEGY_SYMBOL=ETHUSD.P
STRATEGY_RESOLUTION=5
STRATEGY_TP1_RR=1.5
STRATEGY_TP2_RR=3.0
STRATEGY_USE_BE=True
STRATEGY_USE_LIQ_EXIT=True
STRATEGY_USE_ZLSMA_EXIT=True
FLASK_ENV=production
RUN_BACKGROUND_DAEMON=true
EOF
fi

# 7. Configure CloudWatch Agent
if [ -f "$APP_DIR/deploy/cloudwatch_config.json" ]; then
    echo "[INFO] Applying CloudWatch Unified Agent configuration..."
    /opt/aws/amazon-cloudwatch-agent/bin/amazon-cloudwatch-agent-ctl \
        -a fetch-config \
        -m ec2 \
        -s \
        -c file:"$APP_DIR/deploy/cloudwatch_config.json" || echo "[WARN] CloudWatch agent could not connect yet."
fi

# 8. Setup Systemd Services
mkdir -p /var/log/delta-bot
chmod 755 /var/log/delta-bot

if [ -f "$APP_DIR/deploy/systemd/delta-bot.service" ]; then
    echo "[INFO] Installing systemd service delta-bot.service..."
    cp "$APP_DIR/deploy/systemd/delta-bot.service" /etc/systemd/system/delta-bot.service
    systemctl daemon-reload
    systemctl enable delta-bot.service
fi

cat << "EOF_LOGGER" > /etc/systemd/system/delta-bot-logger.service
[Unit]
Description=Stream Docker logs to /var/log/delta-bot/app.log
After=docker.service
Requires=docker.service

[Service]
Type=simple
ExecStart=/bin/sh -c "/usr/bin/docker logs -f delta-bot-app >> /var/log/delta-bot/app.log 2>&1"
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF_LOGGER
systemctl daemon-reload
systemctl enable --now delta-bot-logger.service 2>/dev/null || true

# 9. Build and Start Container Stack
echo "[INFO] Launching Docker build..."
DOCKER_BUILDKIT=0 docker build -t delta-bot-app .
echo "[INFO] Starting Docker Compose stack..."
docker compose up -d

# 10. Seed Database for DA3 Demonstration
echo "[INFO] Seeding paper trading accounts, historical logs, and mock positions..."
docker compose exec -T app python seed_mock_data.py || echo "[WARN] Seeding command executed or will run on first web request."

echo "=========================================================="
echo " [SUCCESS] Delta Trading Bot Deployment Complete!"
if [ -n "$SSL_DOMAIN" ]; then
    echo " Browser-Trusted HTTPS URL: https://${SSL_DOMAIN}/dashboard"
fi
echo " Direct HTTPS URL: https://${PUBLIC_IP:-YOUR_EC2_PUBLIC_IP}/dashboard"
echo " Webhook Endpoint: https://${SSL_DOMAIN:-$PUBLIC_IP}/webhook"
echo "=========================================================="
