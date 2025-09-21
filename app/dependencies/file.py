# /app/dependencies/file.py (Versión Mejorada y Definitiva)

"""
Dependencias relacionadas con la manipulación y validación de archivos.
"""
import logging
from fastapi import UploadFile, HTTPException, status, File
from app.core.config import settings
from app.core.error_code import ErrorCode

# Usamos el logger centralizado que ya configuramos
logger = logging.getLogger("app.dependencies")


async def validate_uploaded_file(file: UploadFile = File(...)) -> UploadFile:
    """
    Dependencia de FastAPI para validar un archivo subido.

    Verifica que el archivo cumpla con los requisitos de tipo MIME y tamaño
    definidos en la configuración de la aplicación. Esta es la forma eficiente
    y "nativa" de FastAPI para manejar validaciones que solo aplican a
    ciertos endpoints.

    Args:
        file (UploadFile): El archivo inyectado por FastAPI. `File(...)` lo hace obligatorio.

    Raises:
        HTTPException (415): Si el tipo de archivo no está permitido.
        HTTPException (413): Si el archivo excede el tamaño máximo permitido.

    Returns:
        UploadFile: El mismo objeto de archivo (rebobinado) si la validación es exitosa.
    """
    # 1. Validar tipo de archivo (MIME type)
    if file.content_type not in settings.ALLOWED_MIME_TYPES:
        logger.warning(
            f"Intento de subida de archivo con tipo no permitido: {file.content_type}"
        )
        raise HTTPException(
            status_code=status.HTTP_415_UNSUPPORTED_MEDIA_TYPE,
            detail={
                "error_code": ErrorCode.VALIDATION_ERROR,
                "message": f"Tipo de archivo no permitido. Permitidos: {list(settings.ALLOWED_MIME_TYPES)}"
            }
        )

    # 2. Validar tamaño del archivo de forma segura
    # Leemos el contenido para obtener el tamaño real y luego lo "rebobinamos"
    # Esto es más seguro que confiar en la cabecera 'content-length'.
    data = await file.read()
    file_size = len(data)
    max_size_bytes = settings.MAX_FILE_SIZE_MB * 1024 * 1024

    if file_size > max_size_bytes:
        logger.warning(
            f"Intento de subida de archivo demasiado grande: {file_size} bytes"
        )
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail={
                "error_code": ErrorCode.PAYLOAD_TOO_LARGE,
                "message": f"El archivo es demasiado grande. Tamaño máximo: {settings.MAX_FILE_SIZE_MB}MB."
            }
        )

    # 3. CRÍTICO: Rebobinar el archivo para que la lógica de la ruta pueda leerlo desde el principio
    await file.seek(0)

    logger.info(f"Archivo '{file.filename}' validado correctamente ({file_size} bytes).")
    return file