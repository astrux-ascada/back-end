# /app/configuration/service.py
"""
Capa de Servicio para el módulo de Configuración.
"""
from typing import List, Optional
from sqlalchemy.orm import Session

from app.configuration import models, schemas
from app.configuration.repository import ConfigurationRepository
from app.core.exceptions import NotFoundException, ConflictException
from app.auditing.service import AuditService
from app.identity.models import User

class ConfigurationService:
    """Servicio de negocio para la gestión de la configuración del sistema."""

    def __init__(self, db: Session, audit_service: AuditService):
        self.db = db
        self.audit_service = audit_service
        self.config_repo = ConfigurationRepository(self.db)

    def create_parameter(self, param_in: schemas.ConfigurationParameterCreate, user: User) -> models.ConfigurationParameter:
        existing_param = self.config_repo.get_parameter(param_in.key, include_inactive=True)
        if existing_param:
            raise ConflictException(f"El parámetro de configuración con la clave '{param_in.key}' ya existe.")
        
        param = self.config_repo.create_parameter(param_in)
        self.audit_service.log_operation(user, "CREATE_CONFIG_PARAMETER", param)
        return param

    def get_parameter(self, key: str) -> models.ConfigurationParameter:
        param = self.config_repo.get_parameter(key)
        if not param:
            raise NotFoundException("Parámetro de configuración no encontrado.")
        return param

    def list_parameters(self) -> List[models.ConfigurationParameter]:
        return self.config_repo.list_parameters()

    def update_parameter(self, key: str, param_in: schemas.ConfigurationParameterUpdate, user: User) -> models.ConfigurationParameter:
        db_param = self.get_parameter(key)
        if not db_param.is_editable:
            raise ConflictException("Este parámetro de configuración no es editable.")
            
        updated_param = self.config_repo.update_parameter(db_param, param_in.value)
        self.audit_service.log_operation(user, "UPDATE_CONFIG_PARAMETER", updated_param, details={"new_value": param_in.value})
        return updated_param

    def delete_parameter(self, key: str, user: User) -> models.ConfigurationParameter:
        db_param = self.get_parameter(key)
        deleted_param = self.config_repo.delete_parameter(db_param)
        self.audit_service.log_operation(user, "DELETE_CONFIG_PARAMETER", deleted_param)
        return deleted_param
