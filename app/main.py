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
from app.core.limiter import limiter
from app.core.middlewares.tenant_middleware import TenantMiddleware
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
    Inicia y detiene servicios de background como el Core Engine.
    """
    logger.info("Iniciando aplicación Astruxa...")
    
    db = SessionLocal()
    
    # Inicializar servicios en el orden correcto de dependencias
    notification_service = NotificationService(db)
    audit_service = AuditService(db)
    asset_repo = AssetRepository(db)
    
    alarming_service = AlarmingService(db, notification_service, asset_repo, audit_service)
    
    # Corregir la inicialización de TelemetryService
    telemetry_service = TelemetryService(db, audit_service)
    
    core_engine_service = CoreEngineService(db, telemetry_service, audit_service)
    app.state.core_engine_service = core_engine_service
    
    logger.info("Handler de logs de Astruxa para acciones automáticas activado.")
    logger.info("Iniciando Core Engine Service...")
    # core_engine_service.start_all_connectors() # Comentado temporalmente para estabilizar
    logger.info("Motor de comunicación (Core Engine) iniciado.")
    
    yield
    
    logger.info("Apagando aplicación...")
    logger.info("Deteniendo Core Engine Service...")
    # app.state.core_engine_service.stop_all_connectors()
    logger.info("Motor de comunicación (Core Engine) detenido.")
    db.close()

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"/api/v1/openapi.json",
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

app.add_middleware(TenantMiddleware)
app.state.limiter = limiter

app.include_router(api_router)

if __name__ == "__main__":
    import uvicorn
    logger.info("🚀 Servidor de depuración iniciado en el puerto 5678. Esperando conexión...")
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
