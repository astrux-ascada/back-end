# /app/main.py
"""
Punto de entrada principal de la aplicación FastAPI de Astruxa.
"""
import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from app.api.v1.routers import api_router
from app.core.config import settings
from app.core.database import SessionLocal
from app.core.redis import get_redis_client
from app.core.limiter import limiter
# from app.core.middlewares.tenant_middleware import TenantMiddleware # DESACTIVADA
from app.core.event_broker import EventBroker
from app.core_engine.service import CoreEngineService
from app.telemetry.service import TelemetryService
from app.auditing.service import AuditService
from app.alarming.service import AlarmingService
from app.notifications.service import NotificationService
from app.assets.repository import AssetRepository

logger = logging.getLogger("app.main")

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Gestiona el ciclo de vida de la aplicación.
    """
    logger.info("Iniciando aplicación Astruxa...")
    
    db = SessionLocal()
    redis_client = get_redis_client()
    
    # --- Inicialización del Event Broker (EDA) ---
    event_broker = EventBroker(redis_client)
    app.state.event_broker = event_broker
    
    # --- Inicialización de Servicios ---
    notification_service = NotificationService(db, event_broker)
    audit_service = AuditService(db)
    asset_repo = AssetRepository(db)
    alarming_service = AlarmingService(db, event_broker, asset_repo, audit_service)
    telemetry_service = TelemetryService(db, audit_service)
    core_engine_service = CoreEngineService(db, telemetry_service, audit_service)
    app.state.core_engine_service = core_engine_service
    
    # --- Iniciar procesos de background ---
    event_broker.start_listening()
    await core_engine_service.start_all_connectors()
    
    logger.info("Handler de logs de Astruxa para acciones automáticas activado.")
    logger.info("Motor de comunicación (Core Engine) y Event Broker iniciados.")
    
    yield
    
    logger.info("Apagando aplicación...")
    await app.state.core_engine_service.stop_all_connectors()
    logger.info("Motor de comunicación (Core Engine) detenido.")
    db.close()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url="/api/v1/openapi.json", # URL correcta para el JSON
    docs_url="/api/v1/docs", # URL para Swagger UI
    redoc_url="/api/v1/redoc", # URL para ReDoc
    lifespan=lifespan
)

if settings.BACKEND_CORS_ORIGINS:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

# app.add_middleware(TenantMiddleware) # DESACTIVADA
app.state.limiter = limiter

# Montar el router principal bajo el prefijo /api/v1
app.include_router(api_router, prefix="/api/v1")

if __name__ == "__main__":
    import uvicorn
    logger.info("🚀 Servidor de depuración iniciado en el puerto 5678. Esperando conexión...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
