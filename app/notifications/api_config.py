# /app/notifications/api_config.py
"""
API Router para la configuración del Módulo de Notificaciones.
"""
import uuid
from typing import List
from fastapi import APIRouter, Depends, status

from app.dependencies.auth import get_current_active_user
from app.dependencies.permissions import require_permission
from app.dependencies.services import get_notification_config_service
from . import schemas
from .service_config import NotificationConfigService

# --- Router para Plantillas ---
templates_router = APIRouter(
    prefix="/templates",
    tags=["Notifications - Configuration"],
    dependencies=[Depends(require_permission("notification_config:manage"))]
)

@templates_router.post("/", response_model=schemas.NotificationTemplateRead, status_code=status.HTTP_201_CREATED)
def create_template(template_in: schemas.NotificationTemplateCreate, service: NotificationConfigService = Depends(get_notification_config_service)):
    return service.create_template(template_in)

@templates_router.get("/", response_model=List[schemas.NotificationTemplateRead])
def list_templates(skip: int = 0, limit: int = 100, service: NotificationConfigService = Depends(get_notification_config_service)):
    return service.list_templates(skip, limit)

@templates_router.get("/{template_id}", response_model=schemas.NotificationTemplateRead)
def get_template(template_id: uuid.UUID, service: NotificationConfigService = Depends(get_notification_config_service)):
    return service.get_template(template_id)

@templates_router.patch("/{template_id}", response_model=schemas.NotificationTemplateRead)
def update_template(template_id: uuid.UUID, template_in: schemas.NotificationTemplateUpdate, service: NotificationConfigService = Depends(get_notification_config_service)):
    return service.update_template(template_id, template_in)

@templates_router.delete("/{template_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_template(template_id: uuid.UUID, service: NotificationConfigService = Depends(get_notification_config_service)):
    service.delete_template(template_id)
    return None

# --- Router para Canales ---
channels_router = APIRouter(
    prefix="/channels",
    tags=["Notifications - Configuration"],
    dependencies=[Depends(require_permission("notification_config:manage"))]
)

@channels_router.post("/", response_model=schemas.NotificationChannelRead, status_code=status.HTTP_201_CREATED)
def create_channel(channel_in: schemas.NotificationChannelCreate, service: NotificationConfigService = Depends(get_notification_config_service)):
    return service.create_channel(channel_in)

@channels_router.get("/", response_model=List[schemas.NotificationChannelRead])
def list_channels(skip: int = 0, limit: int = 100, service: NotificationConfigService = Depends(get_notification_config_service)):
    return service.list_channels(skip, limit)

@channels_router.get("/{channel_id}", response_model=schemas.NotificationChannelRead)
def get_channel(channel_id: uuid.UUID, service: NotificationConfigService = Depends(get_notification_config_service)):
    return service.get_channel(channel_id)

@channels_router.patch("/{channel_id}", response_model=schemas.NotificationChannelRead)
def update_channel(channel_id: uuid.UUID, channel_in: schemas.NotificationChannelUpdate, service: NotificationConfigService = Depends(get_notification_config_service)):
    return service.update_channel(channel_id, channel_in)

@channels_router.delete("/{channel_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_channel(channel_id: uuid.UUID, service: NotificationConfigService = Depends(get_notification_config_service)):
    service.delete_channel(channel_id)
    return None

# --- Router para Reglas ---
rules_router = APIRouter(
    prefix="/rules",
    tags=["Notifications - Configuration"],
    dependencies=[Depends(require_permission("notification_config:manage"))]
)

@rules_router.post("/", response_model=schemas.NotificationRuleRead, status_code=status.HTTP_201_CREATED)
def create_rule(rule_in: schemas.NotificationRuleCreate, service: NotificationConfigService = Depends(get_notification_config_service)):
    return service.create_rule(rule_in)

@rules_router.get("/", response_model=List[schemas.NotificationRuleRead])
def list_rules(skip: int = 0, limit: int = 100, service: NotificationConfigService = Depends(get_notification_config_service)):
    return service.list_rules(skip, limit)

@rules_router.get("/{rule_id}", response_model=schemas.NotificationRuleRead)
def get_rule(rule_id: uuid.UUID, service: NotificationConfigService = Depends(get_notification_config_service)):
    return service.get_rule(rule_id)

@rules_router.patch("/{rule_id}", response_model=schemas.NotificationRuleRead)
def update_rule(rule_id: uuid.UUID, rule_in: schemas.NotificationRuleUpdate, service: NotificationConfigService = Depends(get_notification_config_service)):
    return service.update_rule(rule_id, rule_in)

@rules_router.delete("/{rule_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_rule(rule_id: uuid.UUID, service: NotificationConfigService = Depends(get_notification_config_service)):
    service.delete_rule(rule_id)
    return None
