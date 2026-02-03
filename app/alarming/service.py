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
from app.auditing.service import AuditService
from app.identity.models import User

logger = logging.getLogger(__name__)


class AlarmingService:
    """Servicio de negocio para la gestión de reglas y alarmas."""

    def __init__(
        self, 
        db: Session, 
        notification_service: NotificationService, 
        asset_repo: AssetRepository, 
        audit_service: AuditService,
        maintenance_service: Optional[MaintenanceService] = None
    ):
        self.db = db
        self.notification_service = notification_service
        self.asset_repo = asset_repo
        self.audit_service = audit_service
        self.maintenance_service = maintenance_service
        self.alarming_repo = AlarmingRepository(self.db)
        # La carga de reglas ahora debe ser por tenant, por lo que no se puede hacer en el init.

    def load_rules_for_tenant(self, tenant_id: uuid.UUID) -> List[models.AlarmRule]:
        rules = self.alarming_repo.list_all_enabled_rules(tenant_id)
        logger.info(f"{len(rules)} reglas de alerta activas cargadas para el tenant {tenant_id}.")
        return rules

    def create_alarm_rule(self, rule_in: schemas.AlarmRuleCreate, tenant_id: uuid.UUID) -> models.AlarmRule:
        # Validar que el asset pertenece al tenant
        asset = self.asset_repo.get_asset(rule_in.asset_id, tenant_id)
        if not asset:
            raise ValueError(f"Asset with id {rule_in.asset_id} not found in this tenant.")
        
        return self.alarming_repo.create_alarm_rule(rule_in, tenant_id)

    def evaluate_reading(self, reading: SensorReadingCreate, tenant_id: uuid.UUID):
        """Evalúa una lectura de sensor, y si se dispara una alarma, la audita y notifica."""
        active_rules = self.load_rules_for_tenant(tenant_id)

        for rule in active_rules:
            if rule.asset_id == reading.asset_id and rule.metric_name == reading.metric_name:
                condition_met = False
                if rule.condition == ">" and reading.value > rule.threshold:
                    condition_met = True
                elif rule.condition == "<" and reading.value < rule.threshold:
                    condition_met = True
                
                if condition_met:
                    logger.warning(f"¡ALERTA! Regla {rule.id} disparada para el activo {reading.asset_id} con valor {reading.value}")
                    alarm = self.alarming_repo.create_alarm(rule.id, reading.value, tenant_id)
                    
                    self.audit_alarm_creation(alarm)
                    self.notify_relevant_users(alarm, tenant_id)

    def trigger_maintenance_order(self, alarm: models.Alarm, rule: models.AlarmRule):
        """Crea automáticamente una orden de trabajo correctiva."""
        if not self.maintenance_service:
            logger.warning("MaintenanceService no disponible, no se puede crear orden automática.")
            return

        try:
            asset = self.asset_repo.get_asset(rule.asset_id)
            asset_name = asset.name if asset else "Unknown Asset"
            
            order_in = WorkOrderCreate(
                summary=f"Alarma Crítica: {rule.metric_name} en {asset_name}",
                description=f"Orden generada automáticamente por alarma {alarm.id}. Valor disparador: {alarm.triggered_value}. Regla: {rule.condition} {rule.threshold}",
                priority="URGENT",
                category="CORRECTIVE",
                asset_id=rule.asset_id,
                source_trigger={"type": "ALARM", "alarm_id": str(alarm.id), "rule_id": str(rule.id)}
            )
            
            # Crear la orden sin usuario (sistema)
            order = self.maintenance_service.create_order(order_in, current_user=None)
            logger.info(f"Orden de trabajo {order.id} creada automáticamente para alarma {alarm.id}")
            
        except Exception as e:
            logger.error(f"Error al crear orden de trabajo automática: {e}")

    def audit_alarm_creation(self, alarm: models.Alarm, rule: models.AlarmRule):
        """Registra la creación de una alarma en el log de auditoría."""
        self.audit_service.log_operation(
            user=None, # Acción del sistema
            action="ALARM_TRIGGERED",
            entity_type="Alarm",
            entity_id=alarm.id,
            details={"triggering_value": alarm.triggered_value, "severity": rule.severity}
        )

    def notify_relevant_users(self, alarm: models.Alarm, tenant_id: uuid.UUID):
        asset = self.asset_repo.get_asset(alarm.rule.asset_id, tenant_id)
        if not asset or not asset.sector or not asset.sector.users:
            logger.warning(f"No se encontraron usuarios para notificar para la alarma {alarm.id}")
            return

        message = f"Alarma {rule.severity}: {asset.asset_type.name} ({asset.serial_number}) ha superado el umbral. Valor: {alarm.triggered_value:.2f}"
        
        for user in asset.sector.users:
            self.notification_service.create_notification_for_user(
                user_id=user.id,
                message=message,
                type="ALARM",
                reference_id=str(alarm.id)
            )

    def list_active_alarms(self, tenant_id: uuid.UUID) -> List[models.Alarm]:
        return self.alarming_repo.get_active_alarms(tenant_id)

    def acknowledge_alarm(self, alarm_id: uuid.UUID, tenant_id: uuid.UUID) -> Optional[models.Alarm]:
        return self.alarming_repo.acknowledge_alarm(alarm_id, tenant_id)
