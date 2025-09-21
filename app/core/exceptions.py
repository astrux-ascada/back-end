from app.core.error_messages import ErrorMessages


class CustomBaseException(Exception):
    """Clase base para las excepciones personalizadas de la aplicación."""

    pass


class NotFoundException(CustomBaseException):
    """Lanzada cuando un recurso no se encuentra en la base de datos."""

    def __init__(self, detail: str = ErrorMessages.RESOURCE_NOT_FOUND):
        self.detail = detail
        super().__init__(self.detail)


class ConflictException(CustomBaseException):
    """Lanzada cuando hay un conflicto, como un recurso duplicado."""

    def __init__(self, detail: str = ErrorMessages.CONFLICT, context: dict | None = None):
        self.detail = detail
        self.context = context
        super().__init__(self.detail)


class PermissionDeniedException(CustomBaseException):
    """
    Lanzada cuando un usuario autenticado intenta realizar una acción
    para la que no tiene permisos (resulta en un 403 Forbidden).
    """

    def __init__(self, detail: str = ErrorMessages.PERMISSION_DENIED):
        self.detail = detail
        super().__init__(self.detail)


class AuthenticationException(CustomBaseException):
    """
    Lanzada cuando la autenticación falla (ej. token inválido, credenciales incorrectas).
    Resulta en un 401 Unauthorized.
    """

    def __init__(self, detail: str = ErrorMessages.AUTHENTICATION_FAILED):
        self.detail = detail
        super().__init__(self.detail)


class ValidationException(CustomBaseException):
    """
    Lanzada para errores de validación de lógica de negocio (resulta en un 422).
    Útil cuando la validación va más allá de lo que Pydantic puede hacer.
    """

    def __init__(self, detail: str = ErrorMessages.VALIDATION_ERROR):
        self.detail = detail
        super().__init__(self.detail)


class PayloadTooLargeException(CustomBaseException):
    """
    Lanzada cuando el tamaño de una petición (ej. subida de archivo)
    excede el límite configurado (resulta en un 413).
    """

    def __init__(self, detail: str = ErrorMessages.PAYLOAD_TOO_LARGE):
        self.detail = detail
        super().__init__(self.detail)


class DuplicateRegistrationError(ConflictException):
    """Excepción lanzada cuando se intenta registrar un email que ya existe."""

    def __init__(self, email: str):
        self.email = email
        detail = ErrorMessages.DUPLICATE_EMAIL.replace("e_mai_l", email)
        super().__init__(detail=detail, context={"email": email})


class FormatException(ValidationException):
    """Lanzada cuando el formato de un campo es inválido."""

    def __init__(self, detail: str = ErrorMessages.INVALID_FORMAT):
        super().__init__(detail)


class ReferentialIntegrityException(ConflictException):
    """Lanzada cuando una relación referencial falla."""

    def __init__(self, detail: str = ErrorMessages.REFERENTIAL_INTEGRITY):
        super().__init__(detail)


# python
class RateLimitExceededException(CustomBaseException):
    """Lanzada cuando se excede el límite de solicitudes permitido."""

    def __init__(self, detail: str = ErrorMessages.RATE_LIMIT_EXCEEDED):
        self.detail = detail
        super().__init__(self.detail)


# python
class DatabaseConnectionException(CustomBaseException):
    """Lanzada cuando hay problemas de conexión con la base de datos."""

    def __init__(self, detail: str = ErrorMessages.DATABASE_CONNECTION):
        self.detail = detail
        super().__init__(self.detail)


# python
class TimeoutException(CustomBaseException):
    """Lanzada cuando una operación excede el tiempo de espera permitido."""

    def __init__(self, detail: str = ErrorMessages.TIMEOUT):
        self.detail = detail
        super().__init__(self.detail)


# python
class InvalidCredentialsException(CustomBaseException):
    """Lanzada cuando las credenciales proporcionadas son inválidas."""

    def __init__(self, detail: str = ErrorMessages.INVALID_CREDENTIALS):
        self.detail = detail
        super().__init__(self.detail)


# python
class ServiceUnavailableException(CustomBaseException):
    """Lanzada cuando un servicio externo no está disponible."""

    def __init__(self, detail: str = ErrorMessages.SERVICE_UNAVAILABLE):
        self.detail = detail
        super().__init__(self.detail)


class InvalidEmailException(FormatException):
    """Lanzada cuando el correo electrónico proporcionado no es válido."""

    def __init__(self, email: str):
        detail = ErrorMessages.INVALID_EMAIL_FORMAT
        super().__init__(detail=detail)


class DuplicateEntryError(ConflictException):
    """Lanzada cuando se intenta crear una entrada que viola una restricción de unicidad."""

    def __init__(self, detail: str = "La entrada ya existe o viola una restricción de unicidad."):
        super().__init__(detail=detail)


# -- Address --
class AddressNotFoundException(NotFoundException):
    """Lanzada cuando una dirección no se encuentra o no pertenece al usuario."""

    def __init__(self, detail: str = "Dirección no encontrada o no pertenece al usuario."):
        super().__init__(detail)


# -- EmergData --
class EmergDataNotFoundException(NotFoundException):
    """Lanzada cuando los datos de emergencia de un cliente no se encuentran."""

    def __init__(
        self, detail: str = "Los datos de emergencia para este cliente no fueron encontrados."
    ):
        super().__init__(detail)


class EmergDataAlreadyExistsException(ConflictException):
    """Lanzada cuando un cliente intenta crear datos de emergencia por segunda vez."""

    def __init__(
        self,
        detail: str = "Este cliente ya tiene datos de emergencia registrados. Para modificarlos, utilice la ruta de actualización (PUT).",
    ):
        super().__init__(detail)
