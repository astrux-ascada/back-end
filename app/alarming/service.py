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
from app.notifications.service import NotificationService # Importar NotificationService
from app.auditing.service import AuditService
from app.identity.models import User

if TYPE_CHECKING:
    from app.maintenance.service import MaintenanceService

class AlarmingService:
    """Servicio de negocio para la gestión de alarmas y sus reglas."""

    def __init__(
        self, 
        db: Session, 
        notification_service: NotificationService, # Recibir NotificationService
        asset_repo: AssetRepository, 
        audit_service: AuditService,
        maintenance_service: Optional['MaintenanceService'] = None
    ):
        self.db = db
        self.notification_service = notification_service
        self.alarming_repo = AlarmingRepository(db)
        self.asset_repo = asset_repo
        self.audit_service = audit_service
        self.maintenance_service = maintenance_service

    def create_rule(self, rule_in: schemas.AlarmRuleCreate) -> models.AlarmRule:
        return self.alarming_repo.create_rule(rule_in)

    def get_rules_by_asset(self, asset_id: uuid.UUID) -> List[models.AlarmRule]:
        return self.alarming_repo.get_rules_by_asset(asset_id)

    def get_active_alarms(self, tenant_id: uuid.UUID) -> List[models.Alarm]:
        return self.alarming_repo.get_active_alarms(tenant_id)

    def acknowledge_alarm(self, alarm_id: uuid.UUID, user: User) -> models.Alarm:
        alarm = self.alarming_repo.get_alarm(alarm_id)
        if not alarm:
            raise NotFoundException("Alarm not found")
        
        updated_alarm = self.alarming_repo.acknowledge_alarm(alarm, user.id)
        
        self.audit_service.create_log(
            user_id=user.id,
            tenant_id=user.tenant_id,
            action="ALARM_ACKNOWLEDGED",
            details=f"Alarma {alarm_id} reconocida por {user.name}"
        )
        
        return updated_alarm

    def check_and_trigger_alarms(self, asset_id: uuid.UUID, metric_name: str, value: float):
        """
        Verifica si un nuevo valor de telemetría dispara alguna alarma.
        Este método es llamado por TelemetryService.
        """
        rules = self.alarming_repo.get_rules_for_asset_and_metric(asset_id, metric_name)
        for rule in rules:
            if self._evaluate_condition(value, rule.condition, rule.threshold):
                # Verificar si ya existe una alarma activa para esta regla
                if not self.alarming_repo.has_active_alarm(rule.id):
                    self._trigger_alarm(rule, value)

    def _evaluate_condition(self, value: float, condition: str, threshold: float) -> bool:
        if condition == ">": return value > threshold
        if condition == "<": return value < threshold
        if condition == "==": return value == threshold
        return False

    def _trigger_alarm(self, rule: models.AlarmRule, value: float):
        """
        (Método privado) Crea una alarma y envía una notificación.
        """
        alarm = self.alarming_repo.create_alarm(rule.id, value)
        
        # --- Enviar Notificación Directa ---
        # Usamos NotificationService en lugar de EventBroker por ahora
        # TODO: En el futuro, esto podría volver a ser un evento si implementamos EDA completo
        
        # Nota: Aquí necesitaríamos saber a quién notificar. 
        # Por simplicidad, asumiremos que notificamos a todos los usuarios del tenant con rol OPERATOR
        # Pero como NotificationService.create_platform_notification_for_role es para plataforma,
        # necesitaríamos una función similar para tenants.
        # Por ahora, dejaremos este paso pendiente de implementación detallada en NotificationService
        # o simplemente no notificamos hasta tener esa lógica.
        
        pass
