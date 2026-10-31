# ---------- Build stage: install dependencies once ----------
FROM python:3.12-slim AS build

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --prefix=/install -r requirements.txt

# ---------- Runtime stage: small, non-root, healthy ----------
FROM python:3.12-slim

WORKDIR /app

# Bring installed packages from the build stage
COPY --from=build /install /usr/local

# Copy source and data (training needs the CSV)
COPY src/ src/
COPY data/ data/

# Train the model during the build so the image is self-contained
RUN python src/train/train.py

# Non-root user
RUN useradd --create-home appuser
USER appuser

EXPOSE 8000

# Healthcheck hits /health
HEALTHCHECK --interval=30s --timeout=5s --start-period=10s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8000/health')" || exit 1

CMD ["uvicorn", "src.app.main:app", "--host", "0.0.0.0", "--port", "8000"]

