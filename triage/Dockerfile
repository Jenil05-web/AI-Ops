FROM python:3.10-slim

WORKDIR /app

# System deps needed by faiss/xgboost wheels
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Install deps first (better layer caching — only reinstalls if requirements change)
COPY pyproject.toml .
COPY src/ src/
RUN pip install --no-cache-dir -e .
RUN pip install --no-cache-dir fastapi uvicorn

# Copy the rest of the app
COPY models/ models/
COPY data/processed/ data/processed/

EXPOSE 8000

CMD ["uvicorn", "triage.api.main:app", "--host", "0.0.0.0", "--port", "8000", "--app-dir", "src"]

# Why this ordering matters: dependencies are installed before copying the rest of our code — Docker caches each layer,
# so if we only change a .py file (not pyproject.toml), rebuilding skips the slow pip install step entirely.