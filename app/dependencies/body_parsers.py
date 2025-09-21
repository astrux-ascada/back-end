import logging
from typing import Dict

from fastapi import Depends, HTTPException, Request, status
from pydantic import ValidationError

from app.contracts.external.IGoogleTranslateService import IGoogleTranslateService
from app.dependencies.language import get_language_preference
from app.dependencies.services import get_google_translate_service
from app.models.vital_sign import VitalSignType
from app.schemas.vital_sign_schema import VitalSignCreate

logger = logging.getLogger(__name__)

# --- MEJORA: Caché en memoria para los mapas de traducción inversa ---
# Esto evita llamar a la API de Google en cada petición POST, haciéndolo muy eficiente.
# Estructura: {"es": {"Temperatura corporal": "Body Temperature", ...}}
_translation_cache: Dict[str, Dict[str, str]] = {}


async def _get_reverse_translation_map(
    target_lang: str, translator: IGoogleTranslateService
) -> Dict[str, str]:
    """
    Genera y cachea un mapa de traducción inversa para los tipos de signos vitales.
    Mapea un término traducido (ej. 'Temperatura corporal') de vuelta a su
    término canónico en inglés (ej. 'Body Temperature').
    """
    if target_lang in _translation_cache:
        return _translation_cache[target_lang]

    logger.debug(f"Cache miss para idioma '{target_lang}'. Generando nuevo mapa de traducción.")
    original_types = [e.value for e in VitalSignType]
    try:
        translated_types = await translator.translate_batch(
            texts=original_types, target_language=target_lang, source_language="en"
        )
        # Crear el mapa inverso: {"Término en Español": "English Term"}
        reverse_map = dict(zip(translated_types, original_types))
        _translation_cache[target_lang] = reverse_map
        return reverse_map
    except Exception as e:
        logger.error(f"Fallo al generar el mapa de traducción para '{target_lang}': {e}")
        # Devolver un mapa vacío para no bloquear la app. La validación fallará más adelante.
        return {}


async def get_translated_vital_sign_create_body(
    request: Request,
    target_lang: str = Depends(get_language_preference),
    translator: IGoogleTranslateService = Depends(get_google_translate_service),
) -> VitalSignCreate:
    """
    Dependencia que intercepta el cuerpo de la petición para crear un signo vital.
    Traduce el campo 'type' del idioma del usuario de vuelta al valor canónico
    en inglés antes de que la validación de Pydantic se ejecute.
    """
    try:
        body = await request.json()
    except Exception:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cuerpo JSON inválido.")

    # Si el idioma es inglés o el campo 'type' no viene, se procede a la validación normal.
    if target_lang.startswith("en") or "type" not in body:
        try:
            return VitalSignCreate(**body)
        except ValidationError as e:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.errors())

    user_input_type = body.get("type")
    reverse_map = await _get_reverse_translation_map(target_lang, translator)
    canonical_type = reverse_map.get(user_input_type)

    if canonical_type:
        body["type"] = canonical_type

    try:
        return VitalSignCreate(**body)
    except ValidationError as e:
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=e.errors())