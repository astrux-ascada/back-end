# /app/core/context.py
"""
Define las variables de contexto de la aplicación para el aislamiento de peticiones.

Estas variables permiten almacenar información específica de una petición (como el tenant_id
o el user_id del usuario que la realiza) de una manera segura en entornos asíncronos,
evitando que los datos de una petición se filtren a otra.
"""
from contextvars import ContextVar
from typing import Optional
import uuid

# ContextVar para almacenar el UUID del tenant de la petición actual.
# El valor por defecto es None, lo que significa que no hay tenant en el contexto
# a menos que un middleware o dependencia lo establezca.
tenant_id_context: ContextVar[Optional[uuid.UUID]] = ContextVar("tenant_id_context", default=None)

# ContextVar para almacenar el UUID del usuario de la petición actual.
user_id_context: ContextVar[Optional[uuid.UUID]] = ContextVar("user_id_context", default=None)
