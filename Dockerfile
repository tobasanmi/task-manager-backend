# ── Build stage ───────────────────────────────────────────────────────────────
FROM python:3.12-slim AS base

WORKDIR /app

# Install deps first (layer-caching friendly)
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy source
COPY app.py .

# ── Runtime config ─────────────────────────────────────────────────────────────
ENV PORT=5000 \
    APP_ENV=production \
    APP_VERSION=1.0.0

EXPOSE 5000

# Use gunicorn for production
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "--timeout", "60", "app:app"]
