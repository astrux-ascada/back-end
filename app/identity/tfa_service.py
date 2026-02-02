# /app/identity/tfa_service.py
"""
Servicio para la lógica de 2FA (Two-Factor Authentication) usando TOTP.

Encapsula el uso de la librería `pyotp` para generar secretos, crear URLs
para códigos QR y verificar los tokens de un solo uso.
"""

import pyotp

from app.core.config import settings


class TfaService:
    """Servicio de bajo nivel para operaciones TOTP."""

    def generate_secret(self) -> str:
        """Genera un nuevo secreto de 16 caracteres en formato base32."""
        return pyotp.random_base32()

    def get_otpauth_url(self, secret: str, email: str) -> str:
        """
        Genera la URL `otpauth://` para ser usada en un código QR.

        Args:
            secret: El secreto base32 del usuario.
            email: El email del usuario, que se mostrará en la app de autenticación.

        Returns:
            La URL completa para el código QR.
        """
        return pyotp.totp.TOTP(secret).provisioning_uri(
            name=email,
            issuer_name=settings.PROJECT_NAME
        )

    def verify_token(self, secret: str, token: str) -> bool:
        """
        Verifica si un token TOTP es válido para un secreto dado.

        Args:
            secret: El secreto base32 del usuario.
            token: El código de 6 dígitos proporcionado por el usuario.

        Returns:
            True si el token es válido, False en caso contrario.
        """
        totp = pyotp.TOTP(secret)
        return totp.verify(token)
