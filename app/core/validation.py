# /app/core/validation.py
"""
Módulo de validación de seguridad para entradas críticas (Emails, Contraseñas).
"""
import re
from typing import Optional, Dict
from email_validator import validate_email as validate_email_lib, EmailNotValidError

from app.core.exceptions import ValidationException
from app.core.config import settings # Importar settings

# --- Constantes ---
SPECIAL_CHARS = r"!@#$%^&*()-_=+[]{}|;:,.<>?/~`"

def validate_email(email: str) -> str:
    """
    Valida y normaliza una dirección de correo electrónico.
    """
    try:
        valid = validate_email_lib(email, check_deliverability=True)
        return valid.normalized
    except EmailNotValidError as e:
        raise ValidationException(f"Email inválido: {str(e)}")

def validate_password(password: str, user_context: Optional[Dict[str, str]] = None) -> str:
    """
    Valida que una contraseña cumpla con las políticas de seguridad definidas en la configuración.
    """
    if len(password) < settings.PASSWORD_MIN_LENGTH:
        raise ValidationException(f"La contraseña debe tener al menos {settings.PASSWORD_MIN_LENGTH} caracteres.")

    if settings.PASSWORD_REQUIRE_UPPERCASE and not any(c.isupper() for c in password):
        raise ValidationException("La contraseña debe contener al menos una letra mayúscula.")

    if settings.PASSWORD_REQUIRE_LOWERCASE and not any(c.islower() for c in password):
        raise ValidationException("La contraseña debe contener al menos una letra minúscula.")

    if settings.PASSWORD_REQUIRE_NUMBERS and not any(c.isdigit() for c in password):
        raise ValidationException("La contraseña debe contener al menos un número.")

    if settings.PASSWORD_REQUIRE_SPECIAL_CHARS and not any(c in SPECIAL_CHARS for c in password):
        raise ValidationException(f"La contraseña debe contener al menos un carácter especial: {SPECIAL_CHARS}")

    if user_context:
        for key, value in user_context.items():
            if value and len(value) > 3:
                if value.lower() in password.lower():
                    raise ValidationException(f"La contraseña no puede contener su {key}.")
                if key == 'email':
                    local_part = value.split('@')[0]
                    if len(local_part) > 3 and local_part.lower() in password.lower():
                        raise ValidationException("La contraseña no puede contener partes de su email.")

    return password
