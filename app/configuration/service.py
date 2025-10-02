# /app/configuration/service.py
"""
Capa de Servicio para el módulo de Configuración.
"""

from typing import List, Optional

from sqlalchemy.orm import Session

from app.configuration import models, schemas
from app.configuration.repository import ConfigurationRepository


class ConfigurationService:
    """Servicio de negocio para la gestión de la configuración del sistema."""

    def __init__(self, db: Session):
        self.db = db
        self.config_repo = ConfigurationRepository(self.db)

    # --- Métodos para Parámetros ---

    def list_parameters(self) -> List[models.ConfigurationParameter]:
        return self.config_repo.list_parameters()

    def update_parameter(self, key: str, param_in: schemas.ConfigurationParameterUpdate) -> Optional[models.ConfigurationParameter]:
        # Aquí se podría añadir lógica de validación para el valor
        return self.config_repo.update_parameter(key, param_in.value)

    # --- Métodos para Enums Dinámicos ---

    def list_enum_types(self) -> List[models.EnumType]:
        return self.config_repo.list_enum_types()

    def add_value_to_enum(self, enum_name: str, value_in: schemas.EnumValueCreate) -> Optional[models.EnumType]:
        enum_type = self.config_repo.get_enum_type_by_name(enum_name)
        if not enum_type:
            return None
        
        self.config_repo.add_value_to_enum(enum_type.id, value_in)
        # Volvemos a cargar el tipo de enum para devolverlo con el nuevo valor incluido
        return self.config_repo.get_enum_type_by_name(enum_name)
