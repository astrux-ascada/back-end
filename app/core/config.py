# /app/core/config.py
"""
Módulo de Configuración de la Aplicación.

Carga las variables de entorno y las expone a través de un objeto `settings`.
"""
from typing import List, Union
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    """
    Define las variables de entorno para la aplicación.
    """
    # --- Configuración General ---
    ENV: str = "development"
    PROJECT_NAME: str = "Astruxa"
    BASE_URL: str = "http://localhost:8071"
    BACKEND_CORS_ORIGINS: Union[str, List[str]] = "[]"

    # --- Base de Datos (PostgreSQL / TimescaleDB) ---
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    DATABASE_POOL_SIZE: int = 10
    DATABASE_POOL_OVERFLOW: int = 5
    DATABASE_POOL_TIMEOUT: int = 30

    @property
    def DATABASE_URL(self) -> str:
        """Genera la URL de conexión a la base de datos."""
        return f"postgresql+psycopg://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    # --- Cache y Sesiones (Redis) ---
    REDIS_HOST: str
    REDIS_PORT: int = 6379

    # --- Seguridad y Autenticación ---
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    JWT_EXPIRE_MINUTES: int = 1080  # 18 horas
    
    FIRST_SUPERUSER_EMAIL: str
    FIRST_SUPERUSER_PASSWORD: str
    SUPER_ADMIN_ROLE_NAME: str = "GLOBAL_SUPER_ADMIN"
    TENANT_ADMIN_ROLE_NAME: str = "TENANT_ADMIN"

    # Políticas de Contraseña y Bloqueo
    PASSWORD_MIN_LENGTH: int = 12
    PASSWORD_REQUIRE_UPPERCASE: bool = True
    PASSWORD_REQUIRE_LOWERCASE: bool = True
    PASSWORD_REQUIRE_NUMBERS: bool = True
    PASSWORD_REQUIRE_SPECIAL_CHARS: bool = True
    AUTH_MAX_LOGIN_ATTEMPTS: int = 5
    AUTH_LOCKOUT_DURATION_SECONDS: int = 900

    # --- Almacenamiento de Archivos ---
    STORAGE_TYPE: str = "local"
    STORAGE_PATH: str = "/app/storage"
    MAX_FILE_SIZE_MB: int = 10
    S3_BUCKET_NAME: str = ""
    S3_ACCESS_KEY: str = ""
    S3_SECRET_KEY: str = ""
    S3_ENDPOINT_URL: str = ""

    # --- Pasarelas de Pago ---
    PAYPAL_CLIENT_ID: str = ""
    PAYPAL_CLIENT_SECRET: str = ""
    PAYPAL_WEBHOOK_ID: str = ""
    PAYPAL_API_BASE_URL: str = "https://api-m.sandbox.paypal.com" # Sandbox por defecto

    # --- Integraciones Externas ---
    GOOGLE_API_KEY: str = ""

    # Configuración de Pydantic
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
        extra="ignore" # Ignorar variables extra en el .env (como COMPOSE_PROJECT_NAME)
    )

settings = Settings()
