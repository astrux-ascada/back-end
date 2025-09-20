# backend/main.py
from fastapi import FastAPI, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.core import RedisClient
from app.api.api import api_router

app = FastAPI(title="Orquestador Industrial 5.0 - Backend")

# Incluye el enrutador principal de la API con el prefijo /api/v1
app.include_router(api_router, prefix="/api/v1")


@app.get("/health")
async def health_check(db: AsyncSession = Depends(get_db)):
    # Verificar DB
    await db.execute("SELECT 1")
    # Verificar Redis
    redis = RedisClient()
    await redis.set("healthcheck", "ok", ex=10)
    redis_ok = await redis.get("healthcheck") == "ok"
    return {
        "status": "healthy",
        "database": "connected",
        "redis": "connected" if redis_ok else "failed"
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
