# /app/core/config.py
import logging.config
import os
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Any, Union

from pydantic import PostgresDsn, field_validator, ValidationInfo, EmailStr, AnyHttpUrl
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
    BASE_URL: str = "http://localhost:8071"
    BACKEND_CORS_ORIGINS: List[Union[str, AnyHttpUrl]] = []
    GOOGLE_API_KEY: Optional[str] = None

    # --- Configuración de Base de Datos ---
    POSTGRES_HOST: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    POSTGRES_PORT: int = 5432
    DATABASE_URL: Optional[PostgresDsn] = None
    DATABASE_POOL_SIZE: int = 10
    DATABASE_POOL_OVERFLOW: int = 5
    DATABASE_POOL_TIMEOUT: int = 30

    # --- Configuración de Redis ---
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379

    # --- Configuración de JWT ---
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 1080

    # --- Configuración del Superusuario Inicial ---
    FIRST_SUPERUSER_EMAIL: EmailStr
    FIRST_SUPERUSER_PASSWORD: str

    # --- Políticas de Contraseña ---
    PASSWORD_MIN_LENGTH: int = 12
    PASSWORD_REQUIRE_UPPERCASE: bool = True
    PASSWORD_REQUIRE_LOWERCASE: bool = True
    PASSWORD_REQUIRE_NUMBERS: bool = True
    PASSWORD_REQUIRE_SPECIAL_CHARS: bool = True

    # --- Configuración de Almacenamiento (Media Manager) ---
    STORAGE_TYPE: str = "local"
    STORAGE_PATH: Path = ROOT_PATH / "storage"
    MAX_FILE_SIZE_MB: int = 10
    ALLOWED_MIME_TYPES: dict[str, str] = {
        "image/jpeg": "jpg", "image/png": "png", "image/gif": "gif",
        "image/webp": "webp", "application/pdf": "pdf"
    }
    S3_BUCKET_NAME: Optional[str] = None
    S3_ACCESS_KEY: Optional[str] = None
    S3_SECRET_KEY: Optional[str] = None
    S3_ENDPOINT_URL: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=ENV_PATH, case_sensitive=False, extra="ignore"
    )

    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], info: ValidationInfo) -> Any:
        if isinstance(v, str) and "USER" not in v and "HOST" not in v:
            return v.replace("postgresql://", "postgresql+psycopg://")
        if info.data.get("POSTGRES_HOST"):
            return str(PostgresDsn.build(
                scheme="postgresql+psycopg",
                username=info.data.get("POSTGRES_USER"),
                password=info.data.get("POSTGRES_PASSWORD"),
                host=info.data.get("POSTGRES_HOST"),
                port=info.data.get("POSTGRES_PORT"),
                path=str(info.data.get("POSTGRES_DB")).lstrip("/"),
            ))
        raise ValueError("La configuración de la base de datos está incompleta.")

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        return v

    @field_validator("JWT_SECRET")
    @classmethod
    def validate_jwt_secret(cls, v: str, info: ValidationInfo) -> str:
        if info.data.get("ENV") == "production":
            if len(v) < 32:
                raise ValueError("JWT_SECRET debe tener al menos 32 caracteres en producción.")
            if v == "change_this_secret_to_something_secure_and_long":
                raise ValueError("JWT_SECRET no puede ser el valor por defecto en producción.")
        return v

    @field_validator("S3_BUCKET_NAME")
    @classmethod
    def validate_s3_config(cls, v: Optional[str], info: ValidationInfo) -> Optional[str]:
        if info.data.get("STORAGE_TYPE") == "s3" and not v:
            raise ValueError("S3_BUCKET_NAME es requerido cuando STORAGE_TYPE es 's3'.")
        return v

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
    if "*" in settings.BACKEND_CORS_ORIGINS:
        raise ValueError("BACKEND_CORS_ORIGINS no puede contener '*' en producción.")
