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

    def get_parameter(self, key: str, include_inactive: bool = False) -> Optional[models.ConfigurationParameter]:
        query = self.db.query(models.ConfigurationParameter).filter(models.ConfigurationParameter.key == key)
        if not include_inactive:
            query = query.filter(models.ConfigurationParameter.is_active == True)
        return query.first()

    def list_parameters(self, include_inactive: bool = False) -> List[models.ConfigurationParameter]:
        query = self.db.query(models.ConfigurationParameter)
        if not include_inactive:
            query = query.filter(models.ConfigurationParameter.is_active == True)
        return query.all()

    def create_parameter(self, param_in: schemas.ConfigurationParameterCreate) -> models.ConfigurationParameter:
        db_param = models.ConfigurationParameter(**param_in.model_dump())
        self.db.add(db_param)
        self.db.commit()
        self.db.refresh(db_param)
        return db_param

    def update_parameter(self, db_param: models.ConfigurationParameter, value: str) -> models.ConfigurationParameter:
        if db_param.is_editable:
            db_param.value = value
            self.db.commit()
            self.db.refresh(db_param)
        return db_param

    def delete_parameter(self, db_param: models.ConfigurationParameter) -> models.ConfigurationParameter:
        db_param.is_active = False
        self.db.add(db_param)
        self.db.commit()
        self.db.refresh(db_param)
        return db_param

    # --- Métodos para EnumType y EnumValue ---

    def list_enum_types(self) -> List[models.EnumType]:
        return self.db.query(models.EnumType).options(joinedload(models.EnumType.values)).all()

    def get_enum_type_by_name(self, name: str) -> Optional[models.EnumType]:
        return self.db.query(models.EnumType).filter(models.EnumType.name == name).first()

    def add_value_to_enum(self, enum_type_id: uuid.UUID, value_in: schemas.EnumValueCreate) -> models.EnumValue:
        db_value = models.EnumValue(**value_in.model_dump(), enum_type_id=enum_type_id)
        self.db.add(db_value)
        self.db.commit()
        self.db.refresh(db_value)
        return db_value
