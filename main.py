import os
import asyncpg
from fastapi import FastAPI, HTTPException

app = FastAPI()

# Récupération des variables d’environnement
DB_USER     = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST     = os.getenv("DB_HOST")
DB_NAME     = os.getenv("POSTGRES_DB")
DB_PORT     = os.getenv("DB_PORT", "5432")

@app.on_event("startup")
async def startup():
    try:
        app.state.db = await asyncpg.create_pool(
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=int(DB_PORT),
            database=DB_NAME,
        )
    except Exception as e:
        print(f"[ERROR] Cannot connect to database: {e}")
        raise

@app.on_event("shutdown")
async def shutdown():
    await app.state.db.close()

@app.get("/health")
async def health():
    """
    Endpoint de healthcheck pour CapRover.
    """
    return {"status": "ok"}

@app.get("/items")
async def read_items():
    """
    Expose la table items de la base en JSON.
    """
    try:
        rows = await app.state.db.fetch("SELECT id, name FROM items;")
        return [dict(r) for r in rows]
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/")
async def root():
    """
    Landing page simple à la racine pour remplacer la page Nginx par défaut.
    """
    return {"message": "Bienvenue sur votre FastAPI déployée via CapRover !"}
