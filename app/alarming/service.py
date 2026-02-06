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
from app.core.event_broker import EventBroker # Importar EventBroker
from app.auditing.service import AuditService
from app.identity.models import User

if TYPE_CHECKING:
    from app.maintenance.service import MaintenanceService

class AlarmingService:
    """Servicio de negocio para la gestión de alarmas y sus reglas."""

    def __init__(
        self, 
        db: Session, 
        event_broker: EventBroker, # Recibir el broker
        asset_repo: AssetRepository, 
        audit_service: AuditService,
        maintenance_service: Optional['MaintenanceService'] = None
    ):
        self.db = db
        self.event_broker = event_broker
        self.alarming_repo = AlarmingRepository(db)
        self.asset_repo = asset_repo
        self.audit_service = audit_service
        self.maintenance_service = maintenance_service

    # ... (métodos de CRUD para AlarmRule se mantienen igual) ...

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
        (Método privado) Crea una alarma y publica un evento.
        """
        alarm = self.alarming_repo.create_alarm(rule.id, value)
        
        # --- Publicar Evento (EDA) ---
        # En lugar de llamar directamente al servicio de notificaciones,
        # publicamos un evento que cualquier otro servicio puede consumir.
        event_data = {
            "alarm_id": str(alarm.id),
            "asset_id": str(rule.asset_id),
            "severity": rule.severity,
            "content": f"Alarma '{rule.severity}' en {rule.asset.name}: {rule.metric_name} {rule.condition} {rule.threshold} (Valor: {value})",
            "user_id": str(rule.asset.owner_id) if rule.asset.owner_id else None # Asumiendo que el activo tiene un dueño
        }
        self.event_broker.publish("alarm:triggered", event_data)
        # -----------------------------

        # Opcional: También podríamos publicar un evento para crear una OT de mantenimiento correctivo
        # if rule.severity == "critical" and self.maintenance_service:
        #     self.event_broker.publish("maintenance:request_corrective", {"asset_id": str(rule.asset_id), ...})

    # ... (métodos para acknowledge_alarm, etc. se mantienen igual) ...
