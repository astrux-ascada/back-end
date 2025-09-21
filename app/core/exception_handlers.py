# /Users/jac/develop/emergqr/bff_mobil/app/core/exception_handlers.py

import logging

from fastapi import FastAPI, Request, status
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

from app.core.error_code import ErrorCode
from app.core.exceptions import (
    AuthenticationException,
    ConflictException,
    NotFoundException,
    PayloadTooLargeException,
    PermissionDeniedException,
    ValidationException,
)

# --- MEJORA: Logger a nivel de módulo para mejor práctica y eficiencia.
logger = logging.getLogger(__name__)


def add_exception_handlers(app: FastAPI):
    """
    Añade los manejadores de excepciones personalizados a la instancia de la aplicación FastAPI.
    """

    @app.exception_handler(AuthenticationException)
    async def authentication_handler(request: Request, exc: AuthenticationException):
        """Handler para errores de autenticación (401 Unauthorized)."""
        # --- MEJORA: Log de advertencia para monitorear intentos de acceso fallidos.
        logger.exception(
            f"Authentication failed: {exc.detail}. Path: {request.method} {request.url.path}"
        )
        headers = {"WWW-Authenticate": "Bearer"}
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"error_code": ErrorCode.AUTHENTICATION_FAILED, "message": exc.detail},
            headers=headers,
        )

    @app.exception_handler(PermissionDeniedException)
    async def permission_denied_handler(request: Request, exc: PermissionDeniedException):
        """Handler para errores de permisos (403 Forbidden)."""
        # --- MEJORA: Log de advertencia para monitorear problemas de permisos.
        logger.exception(
            f"Permission denied: {exc.detail}. Path: {request.method} {request.url.path}"
        )
        return JSONResponse(
            status_code=status.HTTP_403_FORBIDDEN,
            content={"error_code": ErrorCode.PERMISSION_DENIED, "message": exc.detail},
        )

    @app.exception_handler(NotFoundException)
    async def not_found_exception_handler(request: Request, exc: NotFoundException):
        """Handler para NotFoundException. Devuelve una respuesta 404 con el detalle del error."""
        # --- MEJORA: Log informativo para errores de cliente comunes.
        logger.exception(
            f"Resource not found: {exc.detail}. Path: {request.method} {request.url.path}"
        )
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"error_code": ErrorCode.NOT_FOUND, "message": exc.detail},
        )

    @app.exception_handler(ConflictException)
    async def conflict_exception_handler(request: Request, exc: ConflictException):
        """Handler para ConflictException. Devuelve una respuesta 409 con el detalle del error."""
        # --- MEJORA: Log informativo para conflictos de datos (ej: duplicados).
        logger.exception(f"Conflict error: {exc.detail}. Path: {request.method} {request.url.path}")
        content = {
            "error_code": ErrorCode.CONFLICT,
            "message": exc.detail,
        }
        if exc.context:
            content["context"] = exc.context
        return JSONResponse(
            status_code=status.HTTP_409_CONFLICT,
            content=content,
        )

    @app.exception_handler(PayloadTooLargeException)
    async def payload_too_large_handler(request: Request, exc: PayloadTooLargeException):
        """Handler para cargas útiles demasiado grandes (413)."""
        # --- MEJORA: Log de advertencia, puede ser un cliente mal configurado o un ataque.
        logger.warning(
            f"Payload too large: {exc.detail}. Path: {request.method} {request.url.path}"
        )
        return JSONResponse(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            content={"error_code": ErrorCode.PAYLOAD_TOO_LARGE, "message": exc.detail},
        )

    @app.exception_handler(ValidationException)
    async def validation_exception_handler(request: Request, exc: ValidationException):
        """Handler para errores de validación de negocio (422)."""
        # --- MEJORA: Log informativo para fallos de validación estándar.
        logger.exception(
            f"Validation error: {exc.detail}. Path: {request.method} {request.url.path}"
        )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={"error_code": ErrorCode.VALIDATION_ERROR, "message": exc.detail},
        )

    @app.exception_handler(Exception)
    async def general_exception_handler(request: Request, exc: Exception):
        """Handler para excepciones no controladas. Devuelve un 500 con un mensaje genérico."""
        # --- MEJORA: logger.exception() para incluir el stacktrace automáticamente.
        logger.exception(f"Unhandled exception caught. Path: {request.method} {request.url.path}")
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content={
                "error_code": ErrorCode.UNEXPECTED_ERROR,
                "message": "Ocurrió un error inesperado en el servidor.",
            },
        )

    @app.exception_handler(RequestValidationError)
    async def request_validation_exception_handler(request: Request, exc: RequestValidationError):
        logger.exception(
            f"Request validation error: {exc.errors()}. Path: {request.method} {request.url.path}"
        )
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content={
                "error_code": ErrorCode.VALIDATION_ERROR,
                "message": "Error de validación en la solicitud.",
                "details": exc.errors(),
            },
        )
