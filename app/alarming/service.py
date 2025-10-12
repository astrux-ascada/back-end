# /app/alarming/service.py
"""
Capa de Servicio para el módulo de Alertas.
"""

import logging
from typing import List, Optional
import uuid

from sqlalchemy.orm import Session

from app.alarming import models, schemas
from app.alarming.repository import AlarmingRepository
from app.telemetry.schemas import SensorReadingCreate
from app.notifications.service import NotificationService
from app.assets.repository import AssetRepository
# --- MEJORA: Importar el AuditService para la trazabilidad ---
from app.auditing.service import AuditService

logger = logging.getLogger(__name__)


class AlarmingService:
    """Servicio de negocio para la gestión de reglas y alarmas."""

    def __init__(self, db: Session, notification_service: NotificationService, asset_repo: AssetRepository, audit_service: AuditService):
        self.db = db
        self.notification_service = notification_service
        self.asset_repo = asset_repo
        self.audit_service = audit_service
        self.alarming_repo = AlarmingRepository(self.db)
        self.active_rules: List[models.AlarmRule] = []
        self.load_rules()

    def load_rules(self):
        self.active_rules = self.alarming_repo.list_all_enabled_rules()
        logger.info(f"{len(self.active_rules)} reglas de alerta activas cargadas en memoria.")

    def create_alarm_rule(self, rule_in: schemas.AlarmRuleCreate) -> models.AlarmRule:
        new_rule = self.alarming_repo.create_alarm_rule(rule_in)
        self.load_rules()
        return new_rule

    def evaluate_reading(self, reading: SensorReadingCreate):
        """Evalúa una lectura de sensor, y si se dispara una alarma, la audita y notifica."""
        for rule in self.active_rules:
            if rule.asset_id == reading.asset_id and rule.metric_name == reading.metric_name:
                condition_met = False
                if rule.condition == ">" and reading.value > rule.threshold:
                    condition_met = True
                elif rule.condition == "<" and reading.value < rule.threshold:
                    condition_met = True
                
                if condition_met:
                    logger.warning(f"¡ALERTA! Regla {rule.id} disparada para el activo {reading.asset_id} con valor {reading.value}")
                    alarm = self.alarming_repo.create_alarm(rule.id, reading.value)
                    
                    # --- Auditoría y Notificación ---
                    self.audit_alarm_creation(alarm)
                    self.notify_relevant_users(alarm)

    def audit_alarm_creation(self, alarm: models.Alarm):
        """Registra la creación de una alarma en el log de auditoría."""
        self.audit_service.log_operation(
            user=None, # Acción del sistema
            action="ALARM_TRIGGERED",
            entity=alarm,
            details={"triggering_value": alarm.triggering_value, "severity": alarm.rule.severity}
        )

    def notify_relevant_users(self, alarm: models.Alarm):
        asset = self.asset_repo.get_asset(alarm.rule.asset_id)
        if not asset or not asset.sector or not asset.sector.users:
            logger.warning(f"No se encontraron usuarios para notificar para la alarma {alarm.id}")
            return

        message = f"Alarma {alarm.rule.severity}: {asset.asset_type.name} ({asset.serial_number}) ha superado el umbral. Valor: {alarm.triggering_value:.2f}"
        
        for user in asset.sector.users:
            self.notification_service.create_notification_for_user(
                user_id=user.id,
                message=message,
                type="ALARM",
                reference_id=str(alarm.id)
            )

    def list_active_alarms(self) -> List[models.Alarm]:
        return self.alarming_repo.get_active_alarms()

    def acknowledge_alarm(self, alarm_id: uuid.UUID) -> Optional[models.Alarm]:
        return self.alarming_repo.acknowledge_alarm(alarm_id)
