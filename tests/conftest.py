import pytest
from typing import Generator, Dict
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.main import app
from app.core.database import SessionLocal

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
    assert response.status_code == 200, "Login failed in test setup for admin@demo.com"
    
    token_data = response.json()
    access_token = token_data["access_token"]
    
    return {"Authorization": f"Bearer {access_token}"}
