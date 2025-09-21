import re


def validate_password_strength(password: str) -> str:
    """
    Validador reutilizable para la fortaleza de la contraseña.
    Lanza un ValueError si la contraseña no cumple los criterios.
    """
    if len(password) < 8:
        raise ValueError("La contraseña debe tener al menos 8 caracteres.")
    if not re.search(r"[A-Z]", password):
        raise ValueError("La contraseña debe contener al menos una letra mayúscula.")
    if not re.search(r"[a-z]", password):
        raise ValueError("La contraseña debe contener al menos una letra minúscula.")
    if not re.search(r"\d", password):
        raise ValueError("La contraseña debe contener al menos un número.")
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        raise ValueError("La contraseña debe contener al menos un carácter especial.")
    return password
