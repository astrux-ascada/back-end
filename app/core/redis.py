# /app/core/redis.py
"""
Servicio central para la gestión de la conexión con Redis.

Este módulo inicializa un pool de conexiones y proporciona una función para
obtener un cliente de Redis, asegurando un uso eficiente de los recursos.
"""

import redis
from app.core.config import settings

# --- Creación del Pool de Conexiones ---
# Se crea una única vez cuando la aplicación arranca.
redis_connection_pool = redis.ConnectionPool(
    host=settings.REDIS_HOST,
    port=settings.REDIS_PORT,
    db=0,  # Usamos la base de datos 0 por defecto
    decode_responses=True  # Decodifica las respuestas de bytes a strings (utf-8)
)

# --- Cliente Principal de Redis ---
# Este es el cliente que el resto de la aplicación usará.
redis_client = redis.Redis(connection_pool=redis_connection_pool)


# --- Dependencia para FastAPI ---
def get_redis_client() -> redis.Redis:
    """
    Dependencia de FastAPI que inyecta el cliente de Redis en los endpoints.
    """
    return redis_client
