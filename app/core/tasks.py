"""
Módulo para tareas en segundo plano (background tasks).

Este archivo contiene tareas asíncronas que se ejecutan de forma concurrente
con la aplicación principal de FastAPI, gestionadas por el lifespan manager.
"""
import asyncio
import logging
from datetime import datetime, timedelta
from app.core.config import settings

logger = logging.getLogger(__name__)


async def cleanup_temp_files():
    """
    Tarea en segundo plano que limpia periódicamente los archivos temporales.

    Esta corutina se ejecuta en un bucle infinito para revisar el directorio
    de almacenamiento temporal (`storage/temp`) y eliminar cualquier archivo
    cuya fecha de modificación sea anterior a 24 horas.

    La tarea se pausa durante una hora (`3600` segundos) después de cada ciclo
    de limpieza para evitar un consumo excesivo de recursos.
    """
    logger.info("Iniciando tarea de limpieza de archivos temporales...")
    while True:
        try:
            temp_dir = settings.STORAGE_PATH / "temp"
            if not temp_dir.exists():
                logger.warning(f"El directorio temporal {temp_dir} no existe. Saltando ciclo de limpieza.")
                await asyncio.sleep(3600)  # Esperar una hora antes de reintentar
                continue

            now = datetime.now()
            files_deleted = 0
            for file in temp_dir.glob("*"):
                if file.is_file():  # Asegurarse de que es un archivo
                    file_time = datetime.fromtimestamp(file.stat().st_mtime)
                    if (now - file_time) > timedelta(hours=24):
                        file.unlink()
                        files_deleted += 1
                        logger.debug(f"Archivo temporal eliminado: {file.name}")

            if files_deleted > 0:
                logger.info(f"Limpieza de archivos temporales completada. Se eliminaron {files_deleted} archivos.")

        except Exception as e:
            logger.error(f"Error en la tarea de limpieza de archivos: {e}", exc_info=True)

        # Esperar para el próximo ciclo de limpieza
        await asyncio.sleep(3600)  # Cada hora