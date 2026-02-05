# /tests/core/test_security.py
"""
Tests para las funciones de seguridad del core.
"""
from app.core.security import hash_password, verify_password

def test_password_hashing_and_verification():
    """
    Test para verificar que el hashing y la verificación de contraseñas funcionan.
    """
    password = "my_super_secret_password"
    
    # 1. Hashear la contraseña
    hashed_password = hash_password(password)
    
    # Asegurarse de que el hash no es igual a la contraseña original
    assert hashed_password != password
    
    # 2. Verificar la contraseña correcta
    assert verify_password(password, hashed_password) == True
    
    # 3. Verificar una contraseña incorrecta
    assert verify_password("wrong_password", hashed_password) == False
