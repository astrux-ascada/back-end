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

logger = logging.getLogger(__name__)


class AlarmingService:
    """Servicio de negocio para la gestión de reglas y alarmas."""

    def __init__(self, db: Session):
        self.db = db
        self.alarming_repo = AlarmingRepository(self.db)
        # Cargamos las reglas en memoria para una evaluación rápida.
        # En un sistema real, esto podría usar una caché como Redis.
        self.active_rules: List[models.AlarmRule] = []
        self.load_rules()

    def load_rules(self):
        """Carga o recarga las reglas de alerta activas en la memoria del servicio."""
        self.active_rules = self.alarming_repo.list_all_enabled_rules()
        logger.info(f"{len(self.active_rules)} reglas de alerta activas cargadas en memoria.")

    def create_alarm_rule(self, rule_in: schemas.AlarmRuleCreate) -> models.AlarmRule:
        """Crea una nueva regla de alerta y recarga las reglas en memoria."""
        new_rule = self.alarming_repo.create_alarm_rule(rule_in)
        self.load_rules() # Recargar para que la nueva regla esté activa inmediatamente
        return new_rule

    def evaluate_reading(self, reading: SensorReadingCreate):
        """Evalúa una lectura de sensor contra todas las reglas activas."""
        for rule in self.active_rules:
            if rule.asset_id == reading.asset_id and rule.metric_name == reading.metric_name:
                # Comprobar si la condición se cumple
                condition_met = False
                if rule.condition == ">" and reading.value > rule.threshold:
                    condition_met = True
                elif rule.condition == "<" and reading.value < rule.threshold:
                    condition_met = True
                elif rule.condition == "==" and reading.value == rule.threshold:
                    condition_met = True
                
                if condition_met:
                    # TODO: Añadir lógica para evitar inundación de alarmas (ej. no crear si ya hay una activa para la misma regla)
                    logger.warning(f"¡ALERTA! Regla {rule.id} disparada para el activo {reading.asset_id} con valor {reading.value}")
                    self.alarming_repo.create_alarm(rule.id, reading.value)

    def list_active_alarms(self) -> List[models.Alarm]:
        return self.alarming_repo.get_active_alarms()

    def acknowledge_alarm(self, alarm_id: uuid.UUID) -> Optional[models.Alarm]:
        return self.alarming_repo.acknowledge_alarm(alarm_id)
