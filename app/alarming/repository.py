# /app/alarming/repository.py
"""
Capa de Repositorio para el módulo de Alertas (Alarming).
"""
from typing import List, Optional
import uuid

from sqlalchemy.orm import Session

from app.alarming import models, schemas

class AlarmingRepository:
    """Realiza operaciones CRUD para las reglas de alarma y las alarmas."""

    def __init__(self, db: Session):
        self.db = db

    def create_alarm_rule(self, rule_in: schemas.AlarmRuleCreate, tenant_id: uuid.UUID) -> models.AlarmRule:
        db_rule = models.AlarmRule(**rule_in.model_dump(), tenant_id=tenant_id)
        self.db.add(db_rule)
        self.db.commit()
        self.db.refresh(db_rule)
        return db_rule

    def list_all_enabled_rules(self, tenant_id: uuid.UUID) -> List[models.AlarmRule]:
        return self.db.query(models.AlarmRule).filter(
            models.AlarmRule.is_enabled == True,
            models.AlarmRule.tenant_id == tenant_id
        ).all()

    def create_alarm(self, rule_id: uuid.UUID, triggering_value: float, tenant_id: uuid.UUID) -> models.Alarm:
        db_alarm = models.Alarm(rule_id=rule_id, triggering_value=triggering_value, tenant_id=tenant_id)
        self.db.add(db_alarm)
        self.db.commit()
        self.db.refresh(db_alarm)
        return db_alarm

    def get_active_alarms(self, tenant_id: uuid.UUID) -> List[models.Alarm]:
        return self.db.query(models.Alarm).filter(
            models.Alarm.is_acknowledged == False,
            models.Alarm.tenant_id == tenant_id
        ).all()

    def acknowledge_alarm(self, alarm_id: uuid.UUID, tenant_id: uuid.UUID) -> Optional[models.Alarm]:
        db_alarm = self.db.query(models.Alarm).filter(
            models.Alarm.id == alarm_id,
            models.Alarm.tenant_id == tenant_id
        ).first()
        if db_alarm:
            db_alarm.is_acknowledged = True
            self.db.commit()
            self.db.refresh(db_alarm)
        return db_alarm
