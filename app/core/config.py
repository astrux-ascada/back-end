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
# Cargar .env.test si estamos en un entorno de pruebas, si no, .env
ENV_FILE = ".env.test" if "PYTEST_CURRENT_TEST" in os.environ else ".env"
ENV_PATH = ROOT_PATH / ENV_FILE


class Settings(BaseSettings):
    # --- Configuración de la Aplicación ---
    ENV: str = "development"  # development|testing|production
    PROJECT_NAME: str = "Astruxa"
    BASE_URL: str = "http://localhost:8000"

    # --- MEJORA: Añadir la configuración de CORS que faltaba ---
    BACKEND_CORS_ORIGINS: List[str] = ["*"]

    # Clave para los servicios de Google Cloud (leída desde .env)
    GOOGLE_API_KEY: str | None = None

    # --- URLs para APIs Médicas Externas ---
    # Estas URLs son la base para los servicios de consulta.


    REGISTER_MAX_QUERY: int = 100
    REGISTER_MIN_QUERY: int = 0

    # --- Configuración de Base de Datos ---
    # --- MEJORA: Hacemos los componentes opcionales para dar flexibilidad ---
    # Esto permite que la configuración venga de una única variable DATABASE_URL
    # o de los componentes individuales.
    POSTGRES_HOST: Optional[str] = None
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_DB: Optional[str] = None
    POSTGRES_PORT: int = 5432  # Valor por defecto

    # --- MEJORA: Usamos PostgresDsn para validar la URL de la BD
    # --- URL de la Base de Datos (Construida automáticamente) ---
    # Hacemos el campo opcional a nivel de definición para que el validador
    # pueda construirlo si no se proporciona explícitamente.
    # El validador se asegurará de que el valor no sea None al final.
    DATABASE_URL: Optional[PostgresDsn] = None

    # --- MEJORA CLAVE: Validador para construir la URL de la BD ---
    @field_validator("DATABASE_URL", mode="before")
    @classmethod
    def assemble_db_connection(cls, v: Optional[str], info: ValidationInfo) -> Any:
        # Prioridad 1: Usar DATABASE_URL si ya está definida en el .env.
        if isinstance(v, str):
            # Nos aseguramos de que use el driver moderno psycopg (v3).
            return v.replace("postgresql://", "postgresql+psycopg://")

        # Prioridad 2: Si no, construirla a partir de los componentes POSTGRES_*.
        if (
                info.data.get("POSTGRES_HOST")
                and info.data.get("POSTGRES_USER")
                and info.data.get("POSTGRES_DB")
        ):
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

        # Si llegamos aquí, no hay configuración de BD suficiente para continuar.
        raise ValueError(
            "La configuración de la base de datos está incompleta. "
            "Proporcione la variable `DATABASE_URL` o el conjunto de variables `POSTGRES_...` en su archivo .env"
        )

    # --- Configuración de JWT ---
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 1440  # 24 horas

    # --- Configuración de Almacenamiento ---
    STORAGE_PATH: Path = ROOT_PATH / "storage"
    MAX_FILE_SIZE_MB: int = 10
    # --- CORRECCIÓN: Añadida la variable que faltaba ---
    # Usamos un Set para una búsqueda más eficiente (O(1)).
    ALLOWED_MIME_TYPES: dict[str, str] = {
        "image/jpeg": "jpg",
        "image/png": "png",
        "image/gif": "gif",
        "image/webp": "webp",
    }

    # --- Configuración avanzada de la Base de Datos ---
    DATABASE_POOL_SIZE: int = 10
    DATABASE_POOL_OVERFLOW: int = 5
    DATABASE_POOL_TIMEOUT: int = 30  # segundos

    # Configuración de Pydantic v2 para cargar desde el archivo .env
    model_config = SettingsConfigDict(
        env_file=ENV_PATH,
        # env_prefix="POSTGRES_",  # Prefijo para las variables de BD si se usa PostgresDsn
        case_sensitive=False,  # Las variables de entorno no suelen ser case-sensitive
        extra="ignore",
    )


# Instancia singleton de configuración
settings = Settings()

# --- MEJORA: Configuración de Logging Estructurada ---
# Esto te da control total sobre el formato y nivel de los logs,
# crucial para la trazabilidad que buscas.


# En desarrollo, podemos bajar el nivel a DEBUG para más detalle.
# 1. Definir el directorio de logs en la raíz del proyecto y asegurarse de que exista.
LOGS_DIR = ROOT_PATH / "logs"
LOGS_DIR.mkdir(exist_ok=True)

# 2. Crear un nombre de archivo dinámico con la fecha actual (ej.: 2023-10-27.log).
log_filename = f"{datetime.now().strftime('%Y-%m-%d')}.log"
log_filepath = LOGS_DIR / log_filename

# 3. Actualizar la configuración de logging ANTES de aplicarla.
#    Esto sobreescribe el valor "filename": "app.log" del diccionario original.
LOGGING_CONFIG["handlers"]["file"]["filename"] = log_filepath

# 4. Ajustar el nivel de log según el entorno.
if settings.ENV == "development":
    LOGGING_CONFIG["loggers"]["app"]["level"] = "DEBUG"

# 5. Aplicar la configuración de logging ya modificada.
logging.config.dictConfig(LOGGING_CONFIG)
logger = logging.getLogger("app")  # Usar un logger nombrado para nuestro código


# --- Validación de entorno ---
if settings.ENV == "production":
    logger.info("Aplicación corriendo en entorno de PRODUCCIÓN.")
    # Forzar configuraciones seguras en producción
    if settings.JWT_EXPIRE_MINUTES > 1440:
        logger.warning("El tiempo de expiración del JWT es mayor a 24h, ajustando a 1440 minutos.")
        settings.JWT_EXPIRE_MINUTES = 1440
    # MEJORA: En producción, los secretos NUNCA deberían venir de un archivo .env.
    # Deberían ser inyectados como variables de entorno por el sistema de orquestación (Docker, K8s)
    # o un gestor de secretos (AWS Secrets Manager, Vault).
    if not os.getenv("JWT_SECRET"):
        logger.error("El secreto JWT no está configurado como variable de entorno en producción.")
        raise ValueError("JWT_SECRET debe ser una variable de entorno en producción.")


# --- Métodos útiles ---
def is_testing() -> bool:
    """Verifica si estamos en entorno de testing."""
    return settings.ENV == "testing"
