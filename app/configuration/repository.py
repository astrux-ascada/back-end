# /app/configuration/repository.py
"""
Capa de Repositorio para el módulo de Configuración.
"""

from typing import List, Optional
import uuid

from sqlalchemy.orm import Session, joinedload

from app.configuration import models, schemas


class ConfigurationRepository:
    """Realiza operaciones CRUD para las entidades de configuración."""

    def __init__(self, db: Session):
        self.db = db

    # --- Métodos para ConfigurationParameter ---

    def get_parameter(self, key: str) -> Optional[models.ConfigurationParameter]:
        return self.db.query(models.ConfigurationParameter).filter(models.ConfigurationParameter.key == key).first()

    def list_parameters(self) -> List[models.ConfigurationParameter]:
        return self.db.query(models.ConfigurationParameter).all()

    def update_parameter(self, key: str, value: str) -> Optional[models.ConfigurationParameter]:
        db_param = self.get_parameter(key)
        if db_param and db_param.is_editable:
            db_param.value = value
            self.db.commit()
            self.db.refresh(db_param)
        return db_param

    # --- Métodos para EnumType y EnumValue ---

    def list_enum_types(self) -> List[models.EnumType]:
        """Lista todos los tipos de enum, cargando sus valores asociados."""
        return self.db.query(models.EnumType).options(joinedload(models.EnumType.values)).all()

    def get_enum_type_by_name(self, name: str) -> Optional[models.EnumType]:
        return self.db.query(models.EnumType).filter(models.EnumType.name == name).first()

    def add_value_to_enum(self, enum_type_id: uuid.UUID, value_in: schemas.EnumValueCreate) -> models.EnumValue:
        db_value = models.EnumValue(**value_in.model_dump(), enum_type_id=enum_type_id)
        self.db.add(db_value)
        self.db.commit()
        self.db.refresh(db_value)
        return db_value
