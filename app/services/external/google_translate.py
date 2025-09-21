import asyncio
import logging
from functools import lru_cache
from typing import List

import httpx

# --- MEJORA: Importar la interfaz ---
from app.contracts.external.IGoogleTranslateService import IGoogleTranslateService
from app.core.config import settings
from app.core.exceptions import ServiceUnavailableException

logger = logging.getLogger(__name__)

GOOGLE_TRANSLATE_URL = "https://translation.googleapis.com/language/translate/v2"


class GoogleTranslateService(IGoogleTranslateService):
    """
    Servicio para interactuar con la API de Google Cloud Translation.
    Gestiona un cliente HTTP asíncrono para reutilizar conexiones.
    """

    def __init__(self, api_key: str | None):
        if not api_key:
            # Este caso ahora se maneja en la dependencia, pero lo dejamos por seguridad.
            raise ValueError("La API Key de Google no puede estar vacía.")
        self._api_key = api_key
        # El cliente se inicializará de forma perezosa en la primera llamada
        self._client: httpx.AsyncClient | None = None

    async def _get_client(self) -> httpx.AsyncClient:
        """Inicializa y devuelve el cliente httpx, reutilizando la instancia."""
        if self._client is None:
            self._client = httpx.AsyncClient(
                base_url=GOOGLE_TRANSLATE_URL,
                params={"key": self._api_key},
                timeout=10.0,  # Añadir un timeout por seguridad
            )
        return self._client

    async def translate(
            self, text: str, target_language: str, source_language: str | None = None
    ) -> str:
        """Traduce un texto usando la API de Google. Si falla, devuelve el texto original."""
        # Si el texto está vacío o el idioma de destino es inglés, no hacer nada.
        if not text or target_language.lower().startswith("en"):
            return text

        payload = {"q": text, "target": target_language}
        if source_language:
            payload["source"] = source_language

        try:
            client = await self._get_client()
            response = await client.post(url="", json=payload)
            response.raise_for_status()  # Lanza una excepción para errores HTTP (4xx o 5xx)
            data = response.json()

            # Validar la estructura de la respuesta de Google
            if not data.get("data") or not data["data"].get("translations"):
                logger.warning("Respuesta inesperada de la API de Google: %s", data)
                return text  # Devuelve el texto original si la respuesta no es la esperada

            translated_text = data["data"]["translations"][0]["translatedText"]
            return translated_text
        except (httpx.HTTPStatusError, httpx.RequestError) as e:
            # TODO: Arreglar el problema subyacente (ej. API Key inválida, API no habilitada) y eliminar este manejo de errores.
            logger.warning(
                f"No se pudo traducir el texto '{text}' a '{target_language}'. "
                f"Devolviendo texto original. Error: {e}"
            )
            return text  # Devuelve el texto original en caso de error de comunicación

    async def translate_batch(
            self, texts: List[str], target_language: str, source_language: str | None = None
    ) -> List[str]:
        """
        Traduce una lista de textos de forma concurrente.
        Si alguna traducción falla, se devolverá el texto original para ese elemento.
        """
        if not texts or target_language.lower().startswith("en"):
            return texts

        tasks = [
            self.translate(text, target_language, source_language)
            for text in texts
        ]
        # asyncio.gather ejecuta todas las tareas de traducción al mismo tiempo.
        # Como `translate` ahora maneja sus propios errores, no necesitamos `return_exceptions=True`.
        results = await asyncio.gather(*tasks)
        return results

    async def close(self):
        """Cierra el cliente HTTP si ha sido inicializado."""
        if self._client:
            await self._client.aclose()
            self._client = None


# --- Inyección de Dependencia ---
# Usamos lru_cache para crear una instancia singleton del servicio.
# Esto asegura que solo haya un objeto GoogleTranslateService en toda la app.
@lru_cache()
def get_google_translate_service() -> IGoogleTranslateService:
    """Devuelve una instancia única del servicio de traducción de Google."""
    if not settings.GOOGLE_API_KEY:
        logger.error("GOOGLE_API_KEY no está configurada. El servicio de traducción no funcionará.")
        # Lanzamos la excepción aquí para que la app falle al iniciar si no está configurada.
        raise ServiceUnavailableException(
            "El servicio de traducción no está configurado en el servidor.")
    return GoogleTranslateService(api_key=settings.GOOGLE_API_KEY)
