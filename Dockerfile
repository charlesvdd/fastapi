# Phase de build pour installer les dépendances
FROM python:3.11-slim AS builder
WORKDIR /app
COPY requirements-prod.txt .
RUN pip install --no-cache-dir -r requirements-prod.txt

FROM python:3.11-slim AS runner
WORKDIR /app
RUN echo ">>> Building with CUSTOM Dockerfile <<<"


ENV PORT=80

COPY --from=builder /usr/local /usr/local
COPY . .

EXPOSE 80

CMD ["sh", "-c", "uvicorn main:app --host 0.0.0.0 --port ${PORT:-80}"]
