# /app/schemas/password.py
from pydantic import BaseModel, Field

class PasswordChange(BaseModel):
    """
    Esquema para que un usuario autenticado cambie su contraseña.
    """
    current_password: str = Field(..., description="La contraseña actual del usuario.")
    new_password: str = Field(..., min_length=8, description="La nueva contraseña, debe cumplir con los requisitos de seguridad.")

class ForgotPasswordRequest(BaseModel):
    """
    Esquema para solicitar un restablecimiento de contraseña.
    """
    email: str = Field(..., description="El correo electrónico del usuario que olvidó su contraseña.")

class ResetPasswordRequest(BaseModel):
    """
    Esquema para realizar el restablecimiento de la contraseña con un token.
    """
    token: str = Field(..., description="El token de restablecimiento recibido por correo electrónico.")
    new_password: str = Field(..., min_length=8, description="La nueva contraseña.")
