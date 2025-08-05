# Phase de build pour installer les dépendances
FROM python:3.11-slim AS builder
WORKDIR /app

# On ne copie que le fichier de prod  
COPY requirements-prod.txt .

# On installe les dépendances de prod
RUN pip install --no-cache-dir -r requirements-prod.txt

# Phase finale, on récupère les dépendances installées
FROM python:3.11-slim AS runner
WORKDIR /app

# On reprend l'environnement Python du builder
COPY --from=builder /usr/local /usr/local

# On copie tout le code de l'app
COPY . .

# On expose le PORT que CapRover définira à runtime
EXPOSE $PORT

# On démarre Uvicorn sur le PORT injecté
CMD ["bash", "-lc", "uvicorn main:app --host 0.0.0.0 --port $PORT"]
