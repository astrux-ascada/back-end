import pytest
from typing import Generator, Dict
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from sqlalchemy import text

from app.main import app
from app.core.database import SessionLocal
from app.identity.models import User, Role
from app.core.security import hash_password
from app.core.config import settings

# Fixture para la sesión de base de datos
@pytest.fixture(scope="session")
def db() -> Generator[Session, None, None]:
    """
    Crea una única sesión de base de datos para toda la sesión de tests.
    """
    # Usamos el engine de la app, que ya está configurado
    from app.core.database import engine
    connection = engine.connect()
    transaction = connection.begin()
    session = SessionLocal(bind=connection)

    yield session

    session.close()
    transaction.rollback()
    connection.close()

# Fixture para el cliente de FastAPI
@pytest.fixture(scope="module")
def client(db: Session) -> Generator[TestClient, None, None]:
    """
    Cliente de pruebas que sobrescribe la dependencia de la BD 
    para usar una sesión de test aislada.
    """
    # Sobrescribir la dependencia get_db
    from app.core.database import get_db
    app.dependency_overrides[get_db] = lambda: db

    with TestClient(app) as c:
        yield c
    
    # Limpiar overrides al final del test
    app.dependency_overrides.clear()

@pytest.fixture(scope="function") # Cambiado a function para aislar tests
def test_user(db: Session) -> Generator[User, None, None]:
    """
    Crea un usuario de prueba para los tests y lo elimina al finalizar.
    """
    email = "test_user_flow@example.com"
    password = "TestPassword123!"
    
    # Limpieza previa por si acaso
    existing_user = db.query(User).filter(User.email == email).first()
    if existing_user:
        # Borrar logs de auditoría antes de borrar el usuario
        db.execute(text("DELETE FROM audit_logs WHERE user_id = :uid"), {"uid": existing_user.id})
        db.delete(existing_user)
        db.commit()
        
    # Crear usuario
    user = User(
        email=email,
        hashed_password=hash_password(password),
        name="Test User Flow",
        is_active=True
    )
    
    # Asignar rol
    role = db.query(Role).filter(Role.name == "GLOBAL_SUPER_ADMIN").first()
    if role:
        user.roles.append(role)
    
    db.add(user)
    db.commit()
    db.refresh(user)
    
    yield user
    
    # Limpieza posterior
    # Borrar logs de auditoría generados durante el test
    db.execute(text("DELETE FROM audit_logs WHERE user_id = :uid"), {"uid": user.id})
    db.delete(user)
    db.commit()

@pytest.fixture(scope="module")
def get_auth_headers(client: TestClient) -> Dict[str, str]:
    """
    Fixture que realiza el login como TENANT ADMIN y devuelve los headers de autorización.
    """
    login_data = {
        "username": "admin@demo.com", # Usar el admin del tenant
        "password": "demo_password"
    }
    response = client.post("/api/v1/auth/login", data=login_data)
    
    # Si falla el login del demo, intentamos con el super admin
    if response.status_code != 200:
        login_data = {
            "username": settings.FIRST_SUPERUSER_EMAIL,
            "password": settings.FIRST_SUPERUSER_PASSWORD
        }
        response = client.post("/api/v1/auth/login", data=login_data)
        
    assert response.status_code == 200, f"Login failed in test setup. Response: {response.text}"
    
    token_data = response.json()
    access_token = token_data["access_token"]
    
    return {"Authorization": f"Bearer {access_token}"}
