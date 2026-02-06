import uuid
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session

from app.assets.models import AssetType

def test_login_and_get_me(client: TestClient, get_auth_headers: dict):
    """
    Smoke Test: Login exitoso y obtención de datos del usuario.
    """
    response_me = client.get("/api/v1/auth/me", headers=get_auth_headers)
    
    assert response_me.status_code == 200
    user_data = response_me.json()
    # CORRECCIÓN: Verificar el email del usuario admin
    assert user_data["email"] == "admin@demo.com"
    assert user_data["is_active"] is True

def test_create_asset_flow(client: TestClient, db: Session, get_auth_headers: dict):
    """
    Test de Integración: Flujo completo de creación de un activo.
    1. Obtiene un AssetType existente de la BD (creado por el seeder).
    2. Crea un Asset usando el tipo anterior.
    3. Verifica que el activo fue creado correctamente.
    """
    # 1. Obtener el AssetType directamente de la BD
    robot_type = db.query(AssetType).filter(AssetType.name == "Robot de Soldadura").first()
    assert robot_type is not None, "El AssetType 'Robot de Soldadura' no fue encontrado en la BD. ¿Corrió el seeder?"
    
    # 2. Crear el Asset
    asset_serial = f"TC-SN-{uuid.uuid4()}"
    asset_data = {
        "asset_type_id": str(robot_type.id),
        "serial_number": asset_serial,
        "location": "Test Bay 1",
        "properties": {"test_run": True}
    }
    response_create = client.post("/api/v1/ops/assets/", headers=get_auth_headers, json=asset_data)
    
    # 3. Verificar la creación
    assert response_create.status_code == 201, f"Failed to create asset: {response_create.text}"
    created_asset = response_create.json()
    
    # El endpoint de Asset devuelve un DTO, así que verificamos los campos del DTO
    assert created_asset["serial_number"] == asset_serial
    assert created_asset["location"] == "Test Bay 1"
    # El DTO puede devolver el objeto AssetType completo o solo su ID.
    # Asumiendo que el DTO anida el AssetType, verificamos su ID.
    # Si el DTO se llama AssetReadDTO y tiene un campo 'asset_type', esto debería funcionar.
    assert created_asset["asset_type"]["id"] == str(robot_type.id)
    assert created_asset["properties"]["test_run"] is True
