# /app/core_engine/service.py
"""
Capa de Servicio para el módulo Core Engine.

Contiene la lógica de negocio para gestionar las fuentes de datos y, en el futuro,
la comunicación en tiempo real con el hardware de la planta.
"""

from typing import List, Optional
import uuid
from sqlalchemy.orm import Session

from app.core_engine import models, schemas
from app.core_engine.repository import CoreEngineRepository


class CoreEngineService:
    """Servicio de negocio para la gestión del motor de comunicación."""

    def __init__(self, db: Session):
        self.db = db
        self.core_engine_repo = CoreEngineRepository(self.db)

    def create_data_source(self, data_source_in: schemas.DataSourceCreate) -> models.DataSource:
        """Crea una nueva configuración de fuente de datos."""
        # Lógica futura: Validar que los connection_params son correctos para el protocolo.
        return self.core_engine_repo.create_data_source(data_source_in)

    def get_data_source(self, data_source_id: uuid.UUID) -> Optional[models.DataSource]:
        """Obtiene una fuente de datos por su ID."""
        return self.core_engine_repo.get_data_source(data_source_id)

    def list_data_sources(self, skip: int = 0, limit: int = 100) -> List[models.DataSource]:
        """Lista todas las fuentes de datos."""
        return self.core_engine_repo.list_data_sources(skip, limit)
