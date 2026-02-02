# /app/alarming/repository.py
"""
Capa de Repositorio para el módulo de Alertas (Alarming).
"""
from typing import List, Optional
import uuid
from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.alarming import models, schemas
from app.telemetry.schemas import SensorReadingCreate

class AlarmingRepository:
    """Realiza operaciones CRUD para las reglas de alarma y las alarmas."""

    def __init__(self, db: Session):
        self.db = db

    def create_alarm_rule(self, rule_in: schemas.AlarmRuleCreate) -> models.AlarmRule:
        db_rule = models.AlarmRule(**rule_in.model_dump())
        self.db.add(db_rule)
        self.db.commit()
        self.db.refresh(db_rule)
        return db_rule

    def list_all_enabled_rules(self) -> List[models.AlarmRule]:
        return self.db.query(models.AlarmRule).filter(models.AlarmRule.is_enabled == True).all()

    def create_alarm(self, rule: models.AlarmRule, reading: SensorReadingCreate) -> models.Alarm:
        db_alarm = models.Alarm(
            alarm_rule_id=rule.id,
            asset_id=reading.asset_id,
            triggered_value=reading.value,
            severity=rule.severity
        )
        self.db.add(db_alarm)
        self.db.commit()
        self.db.refresh(db_alarm)
        return db_alarm

    def get_active_alarms(self) -> List[models.Alarm]:
        # Usamos 'acknowledged' en lugar de 'is_acknowledged'
        return self.db.query(models.Alarm).filter(models.Alarm.acknowledged == False).all()

    def has_active_alarm(self, rule_id: uuid.UUID) -> bool:
        """Verifica si ya existe una alarma activa (no reconocida) para una regla específica."""
        return self.db.query(models.Alarm).filter(
            models.Alarm.alarm_rule_id == rule_id,
            models.Alarm.acknowledged == False
        ).first() is not None

    def acknowledge_alarm(self, alarm_id: uuid.UUID) -> Optional[models.Alarm]:
        db_alarm = self.db.query(models.Alarm).filter(models.Alarm.id == alarm_id).first()
        if db_alarm:
            db_alarm.acknowledged = True
            db_alarm.acknowledged_at = datetime.now(timezone.utc)
            self.db.commit()
            self.db.refresh(db_alarm)
        return db_alarm
