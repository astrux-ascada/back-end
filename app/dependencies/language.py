# /app/dependencies/language.py (NUEVO ARCHIVO)

from typing import Optional

from fastapi import Depends, Header

from app.dependencies.auth import get_current_active_client_or_none
from app.models.client import Client as ClientModel


def get_language_preference(
        accept_language: Optional[str] = Header(None),
        current_client: Optional[ClientModel] = Depends(get_current_active_client_or_none),
) -> str:
    """
    Determina el idioma a utilizar para la respuesta con la siguiente prioridad:
    1. El valor de la cabecera 'Accept-Language'.
    2. El idioma guardado en el perfil del cliente (si está autenticado).
    3. El idioma por defecto del sistema ('en').
    """
    if accept_language:
        # Tomamos la parte principal del idioma, ej: 'es' de 'es-ES,es;q=0.9'
        return accept_language.split(',')[0].split('-')[0].lower()

    if current_client and current_client.preferred_language:
        return current_client.preferred_language

    return "en"  # Idioma por defecto
