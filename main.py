import os
import asyncpg
from fastapi import FastAPI, HTTPException
from starlette.responses import RedirectResponse

app = FastAPI()

# Récupération des variables d’environnement
DB_USER     = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST     = os.getenv("DB_HOST")        # Ne sera set qu’en prod
DB_NAME     = os.getenv("POSTGRES_DB")
DB_PORT     = os.getenv("DB_PORT", "5432")

@app.on_event("startup")
async def startup():
    if DB_HOST:
        try:
            app.state.db = await asyncpg.create_pool(
                user=DB_USER,
                password=DB_PASSWORD,
                host=DB_HOST,
                port=int(DB_PORT),
                database=DB_NAME,
            )
            print("[INFO] Connected to database")
        except Exception as e:
            print(f"[ERROR] Cannot connect to database: {e}")
            app.state.db = None
    else:
        print("[INFO] DB_HOST not set – skipping database connection")

@app.on_event("shutdown")
async def shutdown():
    db = getattr(app.state, "db", None)
    if db:
        await db.close()

@app.get("/health", include_in_schema=False)
async def health():
    return {"status": "ok"}

@app.get("/items")
async def read_items():
    db = getattr(app.state, "db", None)
    if not db:
        raise HTTPException(status_code=503, detail="Database unavailable")
    rows = await db.fetch("SELECT id, name FROM items;")
    return [dict(r) for r in rows]

@app.get("/", include_in_schema=False)
def root():
    return RedirectResponse("/docs")
