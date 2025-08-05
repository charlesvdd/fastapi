import os, asyncpg
from fastapi import FastAPI

app = FastAPI()

DB_USER     = os.getenv("POSTGRES_USER")
DB_PASSWORD = os.getenv("POSTGRES_PASSWORD")
DB_HOST     = os.getenv("DB_HOST")
DB_NAME     = os.getenv("POSTGRES_DB")
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
# …
