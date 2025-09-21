from enum import Enum


class ErrorCode(str, Enum):
    """
    Enumeración de códigos de error para estandarizar las respuestas de la API.
    """
    AUTHENTICATION_FAILED = "authentication_failed"
    CONFLICT = "conflict"
    NOT_FOUND = "not_found"
    PERMISSION_DENIED = "permission_denied"
    INVALID_FORMAT = "invalid_format"  # Para errores 400
    INTEGRITY_VIOLATION = "integrity_violation"  # Para errores 409

    VALIDATION_ERROR = "validation_error"  # Para errores 422
    PAYLOAD_TOO_LARGE = "payload_too_large"  # Para errores 413

    UNEXPECTED_ERROR = "unexpected_error"
    # ... puedes añadir más códigos según sea necesario