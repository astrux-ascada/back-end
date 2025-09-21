class ErrorMessages:
    # --- Errores Generales y de Autenticación ---
    AUTHENTICATION_FAILED = "Credenciales de autenticación no válidas."
    PERMISSION_DENIED = "No tienes permiso para realizar esta acción."
    RESOURCE_NOT_FOUND = "El recurso solicitado no existe."
    CONFLICT = "Ya existe un recurso con los mismos datos."
    VALIDATION_ERROR = "Error de validación en los datos proporcionados."
    PAYLOAD_TOO_LARGE = "La carga útil de la petición es demasiado grande."
    UNEXPECTED_ERROR = "Ocurrió un error inesperado en el servidor."
    INVALID_FORMAT = "El formato del campo es inválido."
    REFERENTIAL_INTEGRITY = "Error de integridad referencial."
    RATE_LIMIT_EXCEEDED = "Se ha excedido el límite de solicitudes permitido."
    DATABASE_CONNECTION = "No se pudo conectar a la base de datos."
    TIMEOUT = "La operación ha excedido el tiempo de espera."
    INVALID_CREDENTIALS = "Las credenciales proporcionadas son inválidas."
    SERVICE_UNAVAILABLE = "El servicio solicitado no está disponible en este momento."
    INVALID_TOKEN = "Token inválido: falta el identificador."
    EXPIRED_TOKEN = "El token ha expirado."  # CORRECCIÓN: "a" -> "ha", "expidrado" -> "expirado"

    # --- Errores Específicos de Dominio ---
    DUPLICATE_EMAIL = "El email {email} ya está registrado."
    INVALID_EMAIL = "El correo electrónico proporcionado no tiene un formato válido."
    DUPLICATE_ENTRY = "La entrada ya existe o viola una restricción de unicidad."

    # --- NUEVOS MENSAJES CENTRALIZADOS ---
    ADDRESS_NOT_FOUND = "Dirección no encontrada o no pertenece al usuario."
    EMERG_DATA_NOT_FOUND = "Los datos de emergencia para este cliente no fueron encontrados."
    EMERG_DATA_ALREADY_EXISTS = "Este cliente ya tiene datos de emergencia registrados. Para modificarlos, utilice la ruta de actualización (PUT)."
