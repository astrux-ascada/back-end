# /app/core/config.py
import logging.config
import os
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Any

from pydantic import PostgresDsn, field_validator, ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict

from app.core.logging_config import LOGGING_CONFIG

# --- Rutas del Proyecto ---
ROOT_PATH = Path(__file__).resolve().parent.parent.parent
ENV_FILE = ".env.test" if "PYTEST_CURRENT_TEST" in os.environ else ".env"
ENV_PATH = ROOT_PATH / ENV_FILE


class Settings(BaseSettings):
    # --- Configuración de la Aplicación ---
    ENV: str = "development"
    PROJECT_NAME: str = "Astruxa"
    BASE_URL: str = "http://localhost:8000"
    BACKEND_CORS_ORIGINS: List[str] = ["*"]
    GOOGLE_API_KEY: Optional[str] = None

    # --- Configuración de Base de Datos ---
    POSTGRES_HOST: Optional[str] = None
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_DB: Optional[str] = None
    POSTGRES_PORT: int = 5432

    DATABASE_URL: Optional[PostgresDsn] = None

    # --- Configuración de Redis ---
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], info: ValidationInfo) -> Any:
        if isinstance(v, str) and "USER" not in v and "HOST" not in v:
            return v.replace("postgresql://", "postgresql+psycopg://")
        
        if info.data.get("POSTGRES_HOST") and info.data.get("POSTGRES_USER") and info.data.get("POSTGRES_DB"):

            return str(
                PostgresDsn.build(
                    scheme="postgresql+psycopg",
                    username=info.data.get("POSTGRES_USER"),
                    password=info.data.get("POSTGRES_PASSWORD"),
                    host=info.data.get("POSTGRES_HOST"),
                    port=info.data.get("POSTGRES_PORT"),
                    path=str(info.data.get("POSTGRES_DB")).lstrip("/"),
                )
            )
raise ValueError("La configuración de la base de datos está incompleta.")

    # --- Configuración de JWT ---
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
 
    JWT_EXPIRE_MINUTES: int = 1080 # 18 horas
 

    # --- Configuración de Almacenamiento ---
    STORAGE_PATH: Path = ROOT_PATH / "storage"
    MAX_FILE_SIZE_MB: int = 10
    ALLOWED_MIME_TYPES: dict[str, str] = {
        "image/jpeg": "jpg",
        "image/png": "png",
        "image/gif": "gif",
        "image/webp": "webp",
    }

    # --- Configuración avanzada de la Base de Datos ---
    DATABASE_POOL_SIZE: int = 10
    DATABASE_POOL_OVERFLOW: int = 5
    DATABASE_POOL_TIMEOUT: int = 30

    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        case_sensitive=False,
        extra="ignore",
    )


settings = Settings()

# --- Configuración de Logging ---
LOGS_DIR = ROOT_PATH / "logs"
LOGS_DIR.mkdir(exist_ok=True)
log_filename = f"{datetime.now().strftime('%Y-%m-%d')}.log"
log_filepath = LOGS_DIR / log_filename
LOGGING_CONFIG["handlers"]["file"]["filename"] = log_filepath
if settings.ENV == "development":
    LOGGING_CONFIG["loggers"]["app"]["level"] = "DEBUG"
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("app")

# --- Validación de entorno ---
if settings.ENV == "production":
    logger.info("Aplicación corriendo en entorno de PRODUCCIÓN.")
    if not os.getenv("JWT_SECRET"):
        logger.error("El secreto JWT no está configurado como variable de entorno en producción.")
        raise ValueError("JWT_SECRET debe ser una variable de entorno en producción.")
