# /app/alarming/repository.py
"""
Capa de Repositorio para el módulo de Alertas.
"""

from typing import List, Optional
import uuid
from datetime import datetime

from sqlalchemy.orm import Session, joinedload

from app.alarming import models, schemas


class AlarmingRepository:
    """Realiza operaciones CRUD para las entidades de Alertas."""

    def __init__(self, db: Session):
        self.db = db

    # --- Métodos para AlarmRule ---

    def create_alarm_rule(self, rule_in: schemas.AlarmRuleCreate) -> models.AlarmRule:
        """Crea una nueva regla de alerta en la base de datos."""
        db_rule = models.AlarmRule(**rule_in.model_dump())
        self.db.add(db_rule)
        self.db.commit()
        self.db.refresh(db_rule)
        return db_rule

    def list_all_enabled_rules(self) -> List[models.AlarmRule]:
        """Obtiene todas las reglas de alerta que están actualmente habilitadas."""
        return self.db.query(models.AlarmRule).filter(models.AlarmRule.is_enabled == True).all()

    # --- Métodos para Alarm ---

    def create_alarm(self, rule_id: uuid.UUID, triggering_value: float) -> models.Alarm:
        """Crea un nuevo registro de Alarma activa."""
        db_alarm = models.Alarm(rule_id=rule_id, triggering_value=triggering_value, status="ACTIVE")
        self.db.add(db_alarm)
        self.db.commit()
        self.db.refresh(db_alarm)
        return db_alarm

    def get_active_alarms(self) -> List[models.Alarm]:
        """Obtiene todas las alarmas que no están en estado 'CLEARED'."""
        return self.db.query(models.Alarm).options(joinedload(models.Alarm.rule)).filter(models.Alarm.status != "CLEARED").all()

    def acknowledge_alarm(self, alarm_id: uuid.UUID) -> Optional[models.Alarm]:
        """Marca una alarma como reconocida (ACKNOWLEDGED)."""
        db_alarm = self.db.query(models.Alarm).filter(models.Alarm.id == alarm_id).first()
        if db_alarm and db_alarm.status == "ACTIVE":
            db_alarm.status = "ACKNOWLEDGED"
            db_alarm.acknowledged_at = datetime.utcnow()
            self.db.commit()
            self.db.refresh(db_alarm)
        return db_alarm
