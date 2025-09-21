import asyncio
import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from slowapi import _rate_limit_exceeded_handler
from slowapi.errors import RateLimitExceeded

from app.api.v1.routers import api_router
from app.api.v1.routers.avatars import router as avatars_router
from app.core.config import settings
from app.core.database import SessionLocal
from app.core.exception_handlers import add_exception_handlers
from app.core.limiter import limiter
from app.core.tasks import cleanup_temp_files
from app.services.external.google_translate import get_google_translate_service
# --- MEJORA: Importar los servicios necesarios para el ciclo de vida ---
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
    """Maneja eventos de inicio/cierre de la aplicación."""
    logger.info("Iniciando aplicación...")
    
    # Creamos una sesión de BD dedicada para el ciclo de vida de los servicios.
    db = SessionLocal()
    
    # --- MEJORA: Iniciar el Core Engine con sus dependencias ---
    # 1. Crear la dependencia (TelemetryService)
    telemetry_service = TelemetryService(db)
    # 2. Crear el servicio principal, inyectando la dependencia
    app.state.core_engine_service = CoreEngineService(db, telemetry_service)
    
    try:
        await app.state.core_engine_service.start()
        logger.info("Motor de comunicación (Core Engine) iniciado.")

        # Tareas de inicio existentes
        settings.STORAGE_PATH.mkdir(parents=True, exist_ok=True)
        (settings.STORAGE_PATH / "clients").mkdir(exist_ok=True)
        (settings.STORAGE_PATH / "medical").mkdir(exist_ok=True)
        (settings.STORAGE_PATH / "temp").mkdir(exist_ok=True)
        logger.info("Directorios de almacenamiento verificados.")
        asyncio.create_task(cleanup_temp_files())
        logger.info("Tarea de limpieza de archivos temporales iniciada.")
        
        yield
        
    finally:
        logger.info("Apagando aplicación...")
        # --- MEJORA: Detener el Core Engine ---
        if hasattr(app.state, 'core_engine_service') and app.state.core_engine_service:
            await app.state.core_engine_service.stop()
            logger.info("Motor de comunicación (Core Engine) detenido.")
        
        # Tareas de cierre existentes
        translator_service = get_google_translate_service()
        await translator_service.close()
        logger.info("Conexiones del servicio de traducción cerradas.")
        db.close()


app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    lifespan=lifespan,
    description="Backend for Frontend para la aplicación móvil EmergQR.",
    docs_url="/api/v1/docs" if settings.ENV == "development" else None,
    redoc_url="/api/v1/redoc" if settings.ENV == "development" else None,
    openapi_url="/api/v1/openapi.json" if settings.ENV == "development" else None,
)

# --- Configuración de Middlewares ---

allowed_origins = []
if settings.ENV == "development":
    allowed_origins.extend([
        "http://localhost:3000",
        "http://192.168.1.42:3000",
    ])

if settings.BACKEND_CORS_ORIGINS:
    allowed_origins.extend([str(origin) for origin in settings.BACKEND_CORS_ORIGINS])

if allowed_origins:
    app.add_middleware(
        CORSMiddleware,
        allow_origins=allowed_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

add_exception_handlers(app)

STATIC_PATH = Path(__file__).parent / "assets"
app.mount("/static", StaticFiles(directory=STATIC_PATH), name="static")
app.mount("/storage", StaticFiles(directory=settings.STORAGE_PATH), name="storage")

# --- Inclusión de Routers ---
app.include_router(api_router)
app.include_router(avatars_router, prefix="/api/v1")

if settings.ENV == "development":
    from app.api.v1.routers import dev_tools
    app.include_router(dev_tools.router, prefix="/api/v1")
    logger.info("🛠️  Routers de desarrollo cargados.")


@app.get("/", tags=["Root"])
def root():
    """Endpoint de bienvenida que muestra información básica del servicio."""
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
