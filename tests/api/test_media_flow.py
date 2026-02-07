import uuid
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
import io

from app.identity.models import Tenant

def test_file_upload_flow(client: TestClient, db: Session, get_auth_headers: dict):
    """
    Test de Integración: Flujo completo de subida de un archivo.
    1. Solicita una URL de subida.
    2. Sube un archivo de prueba a la URL local.
    3. Confirma la subida.
    4. Verifica que el estado del MediaItem es AVAILABLE.
    """
    # 1. Solicitar URL de subida
    upload_request_data = {
        "context": "tenant_logo",
        "original_filename": "test_logo.png",
        "content_type": "image/png",
        "size_bytes": 100
    }
    response_request = client.post(
        "/api/v1/ops/media/upload-request",
        headers=get_auth_headers,
        json=upload_request_data
    )
    assert response_request.status_code == 200, f"Request upload failed: {response_request.text}"
    upload_data = response_request.json()
    
    media_item_id = upload_data["media_item_id"]
    upload_url = upload_data["upload_info"]["url"]

    # 2. Subir el archivo de prueba
    # Crear un archivo falso en memoria
    fake_file_content = b"fake-png-content"
    fake_file = io.BytesIO(fake_file_content)
    
    # El `upload_url` es la ruta de la API, ej: /api/v1/ops/media/local-upload/...
    response_upload = client.put(
        upload_url,
        headers=get_auth_headers,
        files={"file": ("test_logo.png", fake_file, "image/png")}
    )
    assert response_upload.status_code == 204, f"File upload failed: {response_upload.text}"

    # 3. Confirmar la subida
    response_confirm = client.post(
        f"/api/v1/ops/media/{media_item_id}/confirm-upload",
        headers=get_auth_headers
    )
    assert response_confirm.status_code == 200, f"Confirm upload failed: {response_confirm.text}"
    
    # 4. Verificar el estado final
    confirmed_media_item = response_confirm.json()
    assert confirmed_media_item["status"] == "AVAILABLE"
    assert confirmed_media_item["original_filename"] == "test_logo.png"
    
    # Opcional: verificar que el archivo existe en el storage (más complejo, para después)
