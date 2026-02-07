# /app/media/storage.py
"""
Capa de Abstracción de Almacenamiento (Storage Abstraction Layer).

Define la interfaz para los servicios de almacenamiento y proporciona implementaciones
concretas (Local, Cloud) y una fábrica para seleccionarlas.
"""
import os
from abc import ABC, abstractmethod
from typing import Dict, BinaryIO

from app.core.config import settings

# --- 1. Interfaz de Almacenamiento ---

class StorageInterface(ABC):
    """Define el contrato que todas las estrategias de almacenamiento deben seguir."""

    @abstractmethod
    def generate_upload_url(self, file_path: str, content_type: str) -> Dict[str, str]:
        """
        Genera una URL presignada para subir un archivo.
        Retorna un diccionario con la URL y los headers necesarios.
        """
        pass

    @abstractmethod
    def save_file(self, file_path: str, file_content: BinaryIO) -> bool:
        """
        Guarda el contenido de un archivo en la ruta especificada.
        (Principalmente para almacenamiento local).
        """
        pass

    @abstractmethod
    def get_download_url(self, file_path: str) -> str:
        """Genera una URL para descargar un archivo."""
        pass

    @abstractmethod
    def delete_file(self, file_path: str) -> bool:
        """Elimina un archivo del almacenamiento."""
        pass

# --- 2. Implementaciones Concretas ---

class LocalStorageStrategy(StorageInterface):
    """Estrategia para almacenar archivos en el sistema de archivos local."""

    def __init__(self, base_path: str = "/app/storage"):
        self.base_path = base_path
        if not os.path.exists(base_path):
            os.makedirs(base_path)

    def generate_upload_url(self, file_path: str, content_type: str) -> Dict[str, str]:
        """
        Para almacenamiento local, el flujo de URL presignada no aplica.
        Devolvemos una URL de API simbólica para que el cliente sepa dónde subir.
        """
        return {
            "url": f"/api/v1/ops/media/local-upload/{file_path}",
            "method": "PUT"
        }

    def save_file(self, file_path: str, file_content: BinaryIO) -> bool:
        """
        Guarda un archivo en el sistema de archivos local, creando los directorios necesarios.
        """
        full_path = os.path.join(self.base_path, file_path)
        directory = os.path.dirname(full_path)

        try:
            # Crear la estructura de directorios si no existe
            os.makedirs(directory, exist_ok=True)

            # Escribir el archivo
            with open(full_path, "wb") as f:
                f.write(file_content.read())
            return True
        except IOError as e:
            # Loggear el error
            print(f"Error guardando archivo en {full_path}: {e}")
            return False

    def get_download_url(self, file_path: str) -> str:
        """Devuelve una ruta local para servir el archivo."""
        # Esto requerirá un endpoint que sirva archivos estáticos desde el directorio de storage.
        return f"/static/storage/{file_path}"

    def delete_file(self, file_path: str) -> bool:
        full_path = os.path.join(self.base_path, file_path)
        if os.path.exists(full_path):
            os.remove(full_path)
            return True
        return False

class CloudStorageStrategy(StorageInterface):
    """
    Estrategia para almacenar archivos en un servicio compatible con S3 (AWS S3, MinIO).
    (Implementación esqueleto)
    """

    def __init__(self):
        pass

    def generate_upload_url(self, file_path: str, content_type: str) -> Dict[str, str]:
        # Lógica de boto3 para generar URL presignada (comentada por ahora)
        return {
            "url": f"https://{settings.S3_BUCKET_NAME}.s3.amazonaws.com/{file_path}",
            "fields": {"Content-Type": content_type, "key": file_path}
        }
    
    def save_file(self, file_path: str, file_content: BinaryIO) -> bool:
        # En S3, no se usa un save_file directo, se usa la URL presignada.
        # Este método podría usarse para subidas desde el backend, pero no es el flujo principal.
        # Lógica de ejemplo: self.s3_client.upload_fileobj(file_content, self.bucket_name, file_path)
        raise NotImplementedError("El guardado directo no es el flujo principal para S3. Use URLs presignadas.")

    def get_download_url(self, file_path: str) -> str:
        return f"https://{settings.S3_BUCKET_NAME}.s3.amazonaws.com/{file_path}"

    def delete_file(self, file_path: str) -> bool:
        return True

# --- 3. Fábrica de Estrategias ---

def get_storage_strategy() -> StorageInterface:
    """
    Fábrica que devuelve la instancia de la estrategia de almacenamiento
    basada en la configuración del entorno.
    """
    storage_type = settings.STORAGE_TYPE
    if storage_type == "local":
        return LocalStorageStrategy(settings.STORAGE_PATH)
    elif storage_type == "s3":
        return CloudStorageStrategy()
    else:
        raise ValueError(f"Tipo de almacenamiento desconocido: {storage_type}")
