# Multi-stage production Dockerfile for Delta Algorithmic Trading Bot
# Base Python image
FROM python:3.11-slim AS builder

WORKDIR /app

# Install build dependencies if needed
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Install python dependencies in virtual environment
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip setuptools wheel && \
    pip install --no-cache-dir -r requirements.txt

# Final runtime image
FROM python:3.11-slim AS runner

WORKDIR /app

# Install runtime dependencies (libpq for postgresql driver, curl for healthchecks)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 \
    curl \
    sqlite3 \
    && rm -rf /var/lib/apt/lists/*

# Copy virtualenv from builder
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV FLASK_APP=app.py

# Create unprivileged user
RUN groupadd -r appuser && useradd -r -g appuser -d /app -s /sbin/nologin appuser

# Copy application source code
COPY --chown=appuser:appuser . .

# Ensure instance directory exists with proper permissions for SQLite persistence
RUN mkdir -p /app/instance && chown -R appuser:appuser /app/instance

# Switch to non-root user
USER appuser

# Expose internal WSGI port
EXPOSE 5000

# Health check to ensure Flask server is responsive
HEALTHCHECK --interval=30s --timeout=5s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:5000/health || exit 1

# Production Gunicorn command: 1 worker process with 4 threads
# (1 worker process ensures strategy_runner_loop and email_polling_loop run as singletons without duplicate trade executions)
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "1", "--threads", "4", "--timeout", "120", "--access-logfile", "-", "--error-logfile", "-", "app:app"]
