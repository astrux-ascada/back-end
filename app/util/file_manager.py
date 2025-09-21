import uuid
from pathlib import Path
import logging # Añadido para logging
import aiofiles # Añadido para operaciones de archivo asíncronas
from app.core.config import settings

logger = logging.getLogger(__name__) # Inicialización del logger

class FileManager:

    @staticmethod
    def generate_unique_name(original_filename):
        # Mejora: Uso de pathlib para obtener la extensión de forma más robusta
        ext = Path(original_filename).suffix.lstrip('.')
        if not ext:
            logger.warning(f"Filename '{original_filename}' has no extension. Generating unique name without it.")
            return uuid.uuid4().hex
        return f"{uuid.uuid4().hex}.{ext}"

    @classmethod
    async def save_client_photo(cls, client_id: str, file): # Convertido a async
        # Bug Fix: Acceso correcto a settings.STORAGE_PATH
        client_dir = settings.STORAGE_PATH / "clients" / f"client_{client_id}"
        client_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Attempting to save client photo for client_id: {client_id}")

        filename = f"profile_{cls.generate_unique_name(file.filename)}"
        filepath = client_dir / filename

        # Bug Fix: Manejo correcto de UploadFile con aiofiles
        try:
            async with aiofiles.open(filepath, "wb") as buffer:
                await buffer.write(await file.read())
            logger.info(f"Client photo saved successfully to: {filepath}")
        except Exception as e:
            logger.error(f"Failed to save client photo {file.filename} for client {client_id}: {e}")
            raise # Re-lanzar la excepción para que sea manejada por el llamador

        # Mejora: Ruta de retorno consistente (sin barra inicial)
        return f"clients/client_{client_id}/{filename}"

    @classmethod
    async def save_medical_image(cls, study_id: str, file, image_type: str): # Convertido a async
        # Bug Fix: Acceso correcto a settings.STORAGE_PATH
        study_dir = settings.STORAGE_PATH / "medical" / f"study_{study_id}"
        study_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Attempting to save medical image for study_id: {study_id}, type: {image_type}")

        filename = f"{image_type}_{cls.generate_unique_name(file.filename)}"
        filepath = study_dir / filename

        # Bug Fix: Manejo correcto de UploadFile con aiofiles
        try:
            async with aiofiles.open(filepath, "wb") as buffer:
                await buffer.write(await file.read())
            logger.info(f"Medical image saved successfully to: {filepath}")
        except Exception as e:
            logger.error(f"Failed to save medical image {file.filename} for study {study_id}: {e}")
            raise # Re-lanzar la excepción para que sea manejada por el llamador

        # Mejora: Ruta de retorno consistente (sin barra inicial)
        return f"medical/study_{study_id}/{filename}"