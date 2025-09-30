import logging
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api.v1.routers import api_router
# --- ELIMINADO: El router de avatares ya no existe en la nueva arquitectura ---
# from app.api.v1.routers.avatars import router as avatars_router
from app.core.config import settings
from app.core.database import SessionLocal
from app.core.exception_handlers import add_exception_handlers
from app.core.limiter import limiter
from app.core_engine.service import CoreEngineService
from app.telemetry.service import TelemetryService

logger = logging.getLogger(__name__)

if settings.ENV == "development":
    try:
        import debugpy

        debugpy.listen(("0.0.0.0", 5678))
        logger.info("🚀 Servidor de depuración iniciado en el puerto 5678. Esperando conexión...")
    except ImportError:
        logger.warning("debugpy no está instalado, la depuración remota no estará disponible.")


@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Iniciando aplicación...")
    db = SessionLocal()
    telemetry_service = TelemetryService(db)
    app.state.core_engine_service = CoreEngineService(db, telemetry_service)

    try:
        await app.state.core_engine_service.start()
        logger.info("Motor de comunicación (Core Engine) iniciado.")
        # Tareas de inicio adicionales...
        yield
    finally:
        logger.info("Apagando aplicación...")
        if hasattr(app.state, 'core_engine_service') and app.state.core_engine_service:
            await app.state.core_engine_service.stop()
            logger.info("Motor de comunicación (Core Engine) detenido.")
        # Tareas de cierre adicionales...
        db.close()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    lifespan=lifespan,
    # --- MEJORA: Descripción actualizada del proyecto ---
    description="Backend para el Orquestador Industrial 5.0 de Astruxa.",
    docs_url="/api/v1/docs" if settings.ENV == "development" else None,
    redoc_url="/api/v1/redoc" if settings.ENV == "development" else None,
    openapi_url="/api/v1/openapi.json" if settings.ENV == "development" else None,
)

# --- Configuración de Middlewares ---
if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
add_exception_handlers(app)

# --- Inclusión de Routers ---
app.include_router(api_router)
# --- ELIMINADO: El router de avatares ya no se incluye ---
# app.include_router(avatars_router, prefix="/api/v1")

if settings.ENV == "development":
    # Lógica para routers de desarrollo...
    pass


@app.get("/", tags=["Root"])
def root():
    return {
        "message": f"Bienvenido al Backend de {settings.PROJECT_NAME}",
        "version": app.version,
        "environment": settings.ENV,
    }


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="debug" if settings.ENV == "development" else "info",
    )
