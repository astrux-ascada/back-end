# /app/media/storage.py
"""
Capa de Abstracción de Almacenamiento (Storage Abstraction Layer).

Define la interfaz para los servicios de almacenamiento y proporciona implementaciones
concretas (Local, Cloud) y una fábrica para seleccionarlas.
"""
import os
from abc import ABC, abstractmethod
from typing import Dict

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
        Para el almacenamiento local, la "URL de subida" es simplemente un endpoint
        interno que el frontend puede usar, aunque el flujo de URL presignada
        está más orientado a la nube. Aquí simulamos el concepto.
        
        Devolvemos una URL relativa que el backend manejará para guardar el archivo.
        Esto es una simplificación para desarrollo. El flujo real de S3 es diferente.
        """
        # En un entorno de desarrollo real, el frontend podría subir a un endpoint
        # específico que guarde el archivo. Aquí, simplemente confirmamos la ruta.
        # La lógica de subida real se manejaría en un endpoint específico si usamos esta estrategia.
        # Por simplicidad del patrón, asumimos que el frontend "sube" y luego confirma.
        
        # La URL que devolvemos es simbólica. El frontend no la usará para un PUT directo.
        # En su lugar, subirá a un endpoint de nuestra API que use esta ruta.
        # Para mantener el patrón, devolvemos una estructura similar a S3.
        return {
            "url": f"/api/v1/ops/media/local-upload/{file_path}", # Endpoint de API para manejar la subida
            "method": "POST" # O PUT, dependiendo de la implementación del endpoint
        }

    def get_download_url(self, file_path: str) -> str:
        """Devuelve una ruta local para servir el archivo."""
        # Esto requerirá un endpoint que sirva archivos estáticos desde el directorio de storage.
        return f"/static/{file_path}"

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
        # Aquí se inicializaría el cliente de S3 (boto3) con las credenciales
        # import boto3
        # self.s3_client = boto3.client(
        #     's3',
        #     aws_access_key_id=settings.S3_ACCESS_KEY,
        #     aws_secret_access_key=settings.S3_SECRET_KEY,
        #     endpoint_url=settings.S3_ENDPOINT_URL # Opcional, para MinIO
        # )
        # self.bucket_name = settings.S3_BUCKET_NAME
        pass

    def generate_upload_url(self, file_path: str, content_type: str) -> Dict[str, str]:
        """Genera una URL presignada de S3 para una subida con PUT."""
        # Lógica de ejemplo con boto3 (actualmente comentada)
        # try:
        #     response = self.s3_client.generate_presigned_post(
        #         Bucket=self.bucket_name,
        #         Key=file_path,
        #         Fields={"Content-Type": content_type},
        #         Conditions=[{"Content-Type": content_type}],
        #         ExpiresIn=3600  # 1 hora
        #     )
        #     return response
        # except Exception as e:
        #     # Loggear el error
        #     return None
        
        # Placeholder mientras no tenemos boto3 configurado
        return {
            "url": f"https://{settings.S3_BUCKET_NAME}.s3.amazonaws.com/{file_path}",
            "fields": {"Content-Type": content_type, "key": file_path}
        }


    def get_download_url(self, file_path: str) -> str:
        # Lógica de ejemplo con boto3
        # url = self.s3_client.generate_presigned_url(
        #     'get_object',
        #     Params={'Bucket': self.bucket_name, 'Key': file_path},
        #     ExpiresIn=3600 # 1 hora
        # )
        # return url
        return f"https://{settings.S3_BUCKET_NAME}.s3.amazonaws.com/{file_path}"


    def delete_file(self, file_path: str) -> bool:
        # Lógica de ejemplo con boto3
        # try:
        #     self.s3_client.delete_object(Bucket=self.bucket_name, Key=file_path)
        #     return True
        # except Exception as e:
        #     return False
        return True

# --- 3. Fábrica de Estrategias ---

def get_storage_strategy() -> StorageInterface:
    """
    Fábrica que devuelve la instancia de la estrategia de almacenamiento
    basada en la configuración del entorno.
    """
    storage_type = settings.STORAGE_TYPE
    if storage_type == "local":
        return LocalStorageStrategy()
    elif storage_type == "s3":
        return CloudStorageStrategy()
    else:
        raise ValueError(f"Tipo de almacenamiento desconocido: {storage_type}")
