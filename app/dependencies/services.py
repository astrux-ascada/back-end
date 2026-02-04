# /app/dependencies/services.py
"""
Dependency Injection for the services of Astruxa's modules.
"""

import redis
from fastapi import Depends
from sqlalchemy.orm import Session

# --- Import core dependency getters ---
from app.core.database import get_db
from app.core.redis import get_redis_client

# --- Import services from Astruxa's modules ---
from app.identity.auth_service import AuthService
from app.identity.role_service import RoleService
from app.identity.tfa_service import TfaService
from app.identity.service_saas import SaasService
from app.assets.service import AssetService
from app.assets.repository import AssetRepository
from app.telemetry.service import TelemetryService
from app.procurement.service import ProcurementService
from app.maintenance.service import MaintenanceService
from app.core_engine.service import CoreEngineService
from app.sectors.service import SectorService
from app.auditing.service import AuditService
from app.auditing.approval_service import ApprovalService
from app.configuration.service import ConfigurationService
from app.alarming.service import AlarmingService
from app.notifications.service import NotificationService
from app.media.service import MediaService


# --- Service Injectors for Astruxa Modules ---

def get_auth_service(db: Session = Depends(get_db), redis_client: redis.Redis = Depends(get_redis_client)) -> AuthService:
    tfa_service = TfaService()
    return AuthService(db=db, redis_client=redis_client, tfa_service=tfa_service)

def get_saas_service(db: Session = Depends(get_db), auth_service: AuthService = Depends(get_auth_service)) -> SaasService:
    return SaasService(db=db, auth_service=auth_service)

def get_audit_service(db: Session = Depends(get_db)) -> AuditService:
    return AuditService(db)

def get_media_service(db: Session = Depends(get_db)) -> MediaService:
    return MediaService(db)

def get_notification_service(db: Session = Depends(get_db)) -> NotificationService:
    return NotificationService(db)

def get_alarming_service(
    db: Session = Depends(get_db), 
    notification_service: NotificationService = Depends(get_notification_service), 
    audit_service: AuditService = Depends(get_audit_service)
) -> AlarmingService:
    asset_repo = AssetRepository(db)
    return AlarmingService(db=db, notification_service=notification_service, asset_repo=asset_repo, audit_service=audit_service)

def get_role_service(db: Session = Depends(get_db)) -> RoleService:
    return RoleService(db)

def get_asset_service(
    db: Session = Depends(get_db), 
    audit_service: AuditService = Depends(get_audit_service)
) -> AssetService:
    approval_service = ApprovalService(db, asset_service=None)
    return AssetService(db=db, audit_service=audit_service, approval_service=approval_service)

def get_approval_service(
    db: Session = Depends(get_db),
    asset_service: AssetService = Depends(get_asset_service)
) -> ApprovalService:
    approval_service = ApprovalService(db, asset_service=asset_service)
    asset_service.approval_service = approval_service
    return approval_service

def get_telemetry_service(
    db: Session = Depends(get_db), 
    audit_service: AuditService = Depends(get_audit_service),
    alarming_service: AlarmingService = Depends(get_alarming_service)
) -> TelemetryService:
    return TelemetryService(db=db, audit_service=audit_service, alarming_service=alarming_service)

def get_procurement_service(db: Session = Depends(get_db)) -> ProcurementService:
    return ProcurementService(db)

def get_maintenance_service(db: Session = Depends(get_db), audit_service: AuditService = Depends(get_audit_service)) -> MaintenanceService:
    return MaintenanceService(db=db, audit_service=audit_service)

def get_core_engine_service(
    db: Session = Depends(get_db), 
    telemetry_service: TelemetryService = Depends(get_telemetry_service), # Inyectar TelemetryService
    audit_service: AuditService = Depends(get_audit_service) # Inyectar AuditService
) -> CoreEngineService:
    return CoreEngineService(db=db, telemetry_service=telemetry_service, audit_service=audit_service)

def get_sector_service(db: Session = Depends(get_db)) -> SectorService:
    return SectorService(db)

def get_configuration_service(db: Session = Depends(get_db)) -> ConfigurationService:
    return ConfigurationService(db)
