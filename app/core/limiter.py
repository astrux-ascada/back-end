# /app/core/limiter.py
from slowapi import Limiter
from slowapi.util import get_remote_address

# Crea una instancia del limitador.
# get_remote_address es una función de utilidad que obtiene la IP del solicitante.
# Esta IP se usará como clave para rastrear las solicitudes.
limiter = Limiter(key_func=get_remote_address)