# /app/notifications/service_config.py
"""
Capa de Servicio para la configuración del Módulo de Notificaciones.
"""
import uuid
from typing import List
from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException, ConflictException
from . import models, schemas

class NotificationConfigService:
    """Servicio de negocio para la gestión de la configuración de notificaciones."""

    def __init__(self, db: Session):
        self.db = db

    # --- Métodos para NotificationTemplate ---

    def create_template(self, template_in: schemas.NotificationTemplateCreate) -> models.NotificationTemplate:
        if self.db.query(models.NotificationTemplate).filter(models.NotificationTemplate.name == template_in.name).first():
            raise ConflictException(f"A template with name '{template_in.name}' already exists.")
        
        db_template = models.NotificationTemplate(**template_in.model_dump())
        self.db.add(db_template)
        self.db.commit()
        self.db.refresh(db_template)
        return db_template

    def get_template(self, template_id: uuid.UUID) -> models.NotificationTemplate:
        template = self.db.query(models.NotificationTemplate).filter(models.NotificationTemplate.id == template_id).first()
        if not template:
            raise NotFoundException("Template not found.")
        return template

    def list_templates(self, skip: int = 0, limit: int = 100) -> List[models.NotificationTemplate]:
        return self.db.query(models.NotificationTemplate).offset(skip).limit(limit).all()

    def update_template(self, template_id: uuid.UUID, template_in: schemas.NotificationTemplateUpdate) -> models.NotificationTemplate:
        db_template = self.get_template(template_id)
        update_data = template_in.model_dump(exclude_unset=True)

        if 'name' in update_data and self.db.query(models.NotificationTemplate).filter(models.NotificationTemplate.name == update_data['name'], models.NotificationTemplate.id != template_id).first():
            raise ConflictException(f"A template with name '{update_data['name']}' already exists.")

        for field, value in update_data.items():
            setattr(db_template, field, value)
        
        self.db.add(db_template)
        self.db.commit()
        self.db.refresh(db_template)
        return db_template

    def delete_template(self, template_id: uuid.UUID):
        db_template = self.get_template(template_id)
        self.db.delete(db_template)
        self.db.commit()
        return

    # --- Métodos para NotificationChannel ---

    def create_channel(self, channel_in: schemas.NotificationChannelCreate) -> models.NotificationChannel:
        if self.db.query(models.NotificationChannel).filter(models.NotificationChannel.name == channel_in.name).first():
            raise ConflictException(f"A channel with name '{channel_in.name}' already exists.")

        db_channel = models.NotificationChannel(**channel_in.model_dump())
        self.db.add(db_channel)
        self.db.commit()
        self.db.refresh(db_channel)
        return db_channel

    def get_channel(self, channel_id: uuid.UUID) -> models.NotificationChannel:
        channel = self.db.query(models.NotificationChannel).filter(models.NotificationChannel.id == channel_id).first()
        if not channel:
            raise NotFoundException("Channel not found.")
        return channel

    def list_channels(self, skip: int = 0, limit: int = 100) -> List[models.NotificationChannel]:
        return self.db.query(models.NotificationChannel).offset(skip).limit(limit).all()

    def update_channel(self, channel_id: uuid.UUID, channel_in: schemas.NotificationChannelUpdate) -> models.NotificationChannel:
        db_channel = self.get_channel(channel_id)
        update_data = channel_in.model_dump(exclude_unset=True)

        if 'name' in update_data and self.db.query(models.NotificationChannel).filter(models.NotificationChannel.name == update_data['name'], models.NotificationChannel.id != channel_id).first():
            raise ConflictException(f"A channel with name '{update_data['name']}' already exists.")

        for field, value in update_data.items():
            setattr(db_channel, field, value)
        
        self.db.add(db_channel)
        self.db.commit()
        self.db.refresh(db_channel)
        return db_channel

    def delete_channel(self, channel_id: uuid.UUID):
        db_channel = self.get_channel(channel_id)
        self.db.delete(db_channel)
        self.db.commit()
        return

    # --- Métodos para NotificationRule ---

    def create_rule(self, rule_in: schemas.NotificationRuleCreate) -> models.NotificationRule:
        if self.db.query(models.NotificationRule).filter(models.NotificationRule.name == rule_in.name).first():
            raise ConflictException(f"A rule with name '{rule_in.name}' already exists.")

        db_rule = models.NotificationRule(**rule_in.model_dump())
        self.db.add(db_rule)
        self.db.commit()
        self.db.refresh(db_rule)
        return db_rule

    def get_rule(self, rule_id: uuid.UUID) -> models.NotificationRule:
        rule = self.db.query(models.NotificationRule).filter(models.NotificationRule.id == rule_id).first()
        if not rule:
            raise NotFoundException("Rule not found.")
        return rule

    def list_rules(self, skip: int = 0, limit: int = 100) -> List[models.NotificationRule]:
        return self.db.query(models.NotificationRule).offset(skip).limit(limit).all()

    def update_rule(self, rule_id: uuid.UUID, rule_in: schemas.NotificationRuleUpdate) -> models.NotificationRule:
        db_rule = self.get_rule(rule_id)
        update_data = rule_in.model_dump(exclude_unset=True)

        if 'name' in update_data and self.db.query(models.NotificationRule).filter(models.NotificationRule.name == update_data['name'], models.NotificationRule.id != rule_id).first():
            raise ConflictException(f"A rule with name '{update_data['name']}' already exists.")

        for field, value in update_data.items():
            setattr(db_rule, field, value)
        
        self.db.add(db_rule)
        self.db.commit()
        self.db.refresh(db_rule)
        return db_rule

    def delete_rule(self, rule_id: uuid.UUID):
        db_rule = self.get_rule(rule_id)
        self.db.delete(db_rule)
        self.db.commit()
        return
