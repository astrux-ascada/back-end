# /app/core/limiter.py
"""
Configuración del Rate Limiter para la aplicación.
"""
from slowapi import Limiter
from app.dependencies.services import get_limiter_key # Usar la nueva función de clave

# Crear una instancia del limiter usando la función de clave personalizada
limiter = Limiter(key_func=get_limiter_key)
