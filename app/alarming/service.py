# /app/alarming/service.py
"""
Capa de Servicio para el módulo de Alertas (Alarming).
"""
from typing import List, Optional, TYPE_CHECKING
import uuid
from sqlalchemy.orm import Session

from app.alarming import models, schemas
from app.alarming.repository import AlarmingRepository
from app.core.exceptions import NotFoundException
from app.assets.repository import AssetRepository
from app.notifications.service import NotificationService
from app.auditing.service import AuditService
from app.identity.models import User

if TYPE_CHECKING:
    from app.maintenance.service import MaintenanceService

class AlarmingService:
    """Servicio de negocio para la gestión de alarmas y sus reglas."""

    def __init__(
        self, 
        db: Session, 
        notification_service: NotificationService, 
        asset_repo: AssetRepository, 
        audit_service: AuditService,
        maintenance_service: Optional['MaintenanceService'] = None
    ):
        self.db = db
        self.alarming_repo = AlarmingRepository(db)
        self.asset_repo = asset_repo
        self.notification_service = notification_service
        self.audit_service = audit_service
        self.maintenance_service = maintenance_service

    # --- Métodos para AlarmRule ---

    def create_alarm_rule(self, rule_in: schemas.AlarmRuleCreate, tenant_id: uuid.UUID, user: User) -> models.AlarmRule:
        asset = self.asset_repo.get_asset(rule_in.asset_id, tenant_id)
        if not asset:
            raise NotFoundException(f"El activo con ID {rule_in.asset_id} no fue encontrado en este tenant.")
        
        new_rule = self.alarming_repo.create_alarm_rule(rule_in, tenant_id)
        
        self.audit_service.log_operation(user, "CREATE_ALARM_RULE", new_rule)
        return new_rule

    def get_rule(self, rule_id: uuid.UUID, tenant_id: uuid.UUID) -> models.AlarmRule:
        rule = self.alarming_repo.get_rule(rule_id, tenant_id)
        if not rule:
            raise NotFoundException("Regla de alarma no encontrada.")
        return rule

    def list_rules(self, tenant_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[models.AlarmRule]:
        return self.alarming_repo.list_rules(tenant_id, skip, limit)

    def update_rule(self, rule_id: uuid.UUID, rule_in: schemas.AlarmRuleUpdate, tenant_id: uuid.UUID, user: User) -> models.AlarmRule:
        db_rule = self.get_rule(rule_id, tenant_id)
        
        if rule_in.asset_id and rule_in.asset_id != db_rule.asset_id:
            asset = self.asset_repo.get_asset(rule_in.asset_id, tenant_id)
            if not asset:
                raise NotFoundException(f"El nuevo activo con ID {rule_in.asset_id} no fue encontrado en este tenant.")

        updated_rule = self.alarming_repo.update_rule(db_rule, rule_in)
        
        self.audit_service.log_operation(user, "UPDATE_ALARM_RULE", updated_rule, details=rule_in.model_dump(exclude_unset=True))
        return updated_rule

    def delete_rule(self, rule_id: uuid.UUID, tenant_id: uuid.UUID, user: User) -> models.AlarmRule:
        db_rule = self.get_rule(rule_id, tenant_id)
        deleted_rule = self.alarming_repo.delete_rule(db_rule)
        
        self.audit_service.log_operation(user, "DELETE_ALARM_RULE", deleted_rule)
        return deleted_rule

    # --- Métodos para Alarm ---

    def get_active_alarms(self, tenant_id: uuid.UUID) -> List[models.Alarm]:
        return self.alarming_repo.get_active_alarms(tenant_id)

    def acknowledge_alarm(self, alarm_id: uuid.UUID, tenant_id: uuid.UUID, user: User) -> models.Alarm:
        alarm = self.alarming_repo.acknowledge_alarm(alarm_id, tenant_id)
        if not alarm:
            raise NotFoundException("Alarma no encontrada o ya reconocida.")
        
        self.audit_service.log_operation(user, "ACKNOWLEDGE_ALARM", alarm)
        return alarm
