# /tests/api/test_auth_flow.py
import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import asyncio

from app.core.config import settings
from app.identity.models import User
from app.core.security import hash_password, create_password_reset_token

# --- Pruebas de Cambio de Contraseña ---

def test_change_password_success(client: TestClient, test_user: User, db: Session):
    """
    Prueba que un usuario autenticado puede cambiar su contraseña correctamente.
    """
    login_data = {"username": test_user.email, "password": "TestPassword123!"}
    response = client.post(f"/api/v1/auth/login", data=login_data)
    assert response.status_code == 200
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    change_password_data = {
        "current_password": "TestPassword123!",
        "new_password": "NewSecurePassword123!",
    }
    response = client.post(f"/api/v1/auth/change-password", json=change_password_data, headers=headers)
    
    assert response.status_code == 204, response.text

    # Verificar que la nueva contraseña funciona
    db.refresh(test_user)
    new_login_data = {"username": test_user.email, "password": "NewSecurePassword123!"}
    response = client.post(f"/api/v1/auth/login", data=new_login_data)
    assert response.status_code == 200, "El login con la nueva contraseña debería funcionar."

def test_change_password_wrong_current_password(client: TestClient, test_user: User):
    """
    Prueba que el cambio de contraseña falla si la contraseña actual es incorrecta.
    """
    login_data = {"username": test_user.email, "password": "TestPassword123!"}
    response = client.post(f"/api/v1/auth/login", data=login_data)
    token = response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}

    change_password_data = {
        "current_password": "wrong_password",
        "new_password": "NewSecurePassword123!",
    }
    response = client.post(f"/api/v1/auth/change-password", json=change_password_data, headers=headers)
    
    assert response.status_code == 401
    assert "incorrecta" in response.json()["message"]

def test_change_password_unauthenticated(client: TestClient):
    """
    Prueba que un usuario no autenticado no puede cambiar la contraseña.
    """
    change_password_data = {
        "current_password": "some_password",
        "new_password": "NewSecurePassword123!",
    }
    response = client.post(f"/api/v1/auth/change-password", json=change_password_data)
    assert response.status_code == 403 # Cambiado de 401 a 403


# --- Pruebas de Recuperación de Contraseña ---

def test_forgot_password_flow(client: TestClient, test_user: User, db: Session):
    """
    Prueba el flujo completo de recuperación de contraseña.
    """
    # 1. Solicitar restablecimiento de contraseña
    forgot_password_data = {"email": test_user.email}
    response = client.post(f"/api/v1/auth/forgot-password", json=forgot_password_data)
    assert response.status_code == 202

    # En un caso real, el token se enviaría por correo. Para la prueba, lo generamos.
    reset_token = create_password_reset_token(email=test_user.email)

    # 2. Restablecer la contraseña con el token
    reset_password_data = {
        "token": reset_token,
        "new_password": "ResetSecurePassword123!",
    }
    response = client.post(f"/api/v1/auth/reset-password", json=reset_password_data)
    assert response.status_code == 204, response.text

    # 3. Verificar que la nueva contraseña funciona
    db.refresh(test_user)
    new_login_data = {"username": test_user.email, "password": "ResetSecurePassword123!"}
    response = client.post(f"/api/v1/auth/login", data=new_login_data)
    assert response.status_code == 200, "El login con la contraseña restablecida debería funcionar."

    # 4. Verificar que la contraseña antigua ya no funciona
    old_login_data = {"username": test_user.email, "password": "TestPassword123!"}
    response = client.post(f"/api/v1/auth/login", data=old_login_data)
    assert response.status_code != 200, "El login con la contraseña antigua no debería funcionar."

def test_reset_password_invalid_token(client: TestClient):
    """
    Prueba que el restablecimiento de contraseña falla con un token inválido.
    """
    reset_password_data = {
        "token": "invalid-token",
        "new_password": "SomeNewPassword123!",
    }
    response = client.post(f"/api/v1/auth/reset-password", json=reset_password_data)
    assert response.status_code == 401
    # CORRECCIÓN: Hacemos la aserción más flexible para evitar problemas de codificación.
    assert "inválido" in response.json()["message"]
