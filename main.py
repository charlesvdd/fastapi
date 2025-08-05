from fastapi import FastAPI
import os
import asyncpg

app = FastAPI()

# Lecture des variables d'env définies dans l'UI CapRover
DB_USER     = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST     = os.getenv("DB_HOST")
DB_NAME     = os.getenv("DB_NAME")
DB_PORT     = os.getenv("DB_PORT", "5432")

@app.on_event("startup")
async def startup():
    app.state.db = await asyncpg.create_pool(
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=int(DB_PORT),
        database=DB_NAME,
    )

@app.on_event("shutdown")
async def shutdown():
    await app.state.db.close()

@app.get("/health")
async def health():
    return {"status": "ok"}

@app.get("/items")
async def read_items():
    rows = await app.state.db.fetch("SELECT id, name FROM items;")
    return [dict(r) for r in rows]
