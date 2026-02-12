# /app/dependencies/services.py
"""
Dependency Injection for the services of Astruxa's modules.
"""

import redis
from fastapi import Depends, Request
from sqlalchemy.orm import Session

from app.alarming.service import AlarmingService
from app.assets.repository import AssetRepository
from app.assets.service import AssetService
from app.auditing.approval_service import ApprovalService
from app.auditing.service import AuditService
from app.configuration.service import ConfigurationService
# --- Import core dependency getters ---
from app.core.database import get_db
from app.core.redis import get_redis_client
from app.core_engine.service import CoreEngineService
# --- Import services from Astruxa's modules ---
from app.identity.auth_service import AuthService
from app.identity.role_service import RoleService
from app.identity.service_partner import PartnerService
from app.identity.service_saas import SaasService
from app.identity.service_usage import UsageService
from app.identity.service_marketing import MarketingService
from app.identity.tfa_service import TfaService
from app.maintenance.service import MaintenanceService
from app.media.service import MediaService
from app.notifications.service import NotificationService
from app.notifications.service_config import NotificationConfigService
from app.payments.service import PaymentService
from app.payments.service_manual import ManualPaymentService
from app.payments.service_online import OnlinePaymentService
from app.procurement.service import ProcurementService
from app.procurement.service_evaluation import EvaluationService
from app.sectors.service import SectorService
from app.telemetry.service import TelemetryService
from app.reporting.service import ReportingService
from app.reporting.stoppage_service import StoppageService


# --- Service Injectors for Astruxa Modules ---

def get_auth_service(db: Session = Depends(get_db),
                     redis_client: redis.Redis = Depends(get_redis_client)) -> AuthService:
    tfa_service = TfaService()
    return AuthService(db=db, redis_client=redis_client, tfa_service=tfa_service)

def get_audit_service(db: Session = Depends(get_db)) -> AuditService:
    return AuditService(db)

def get_notification_service(db: Session = Depends(get_db)) -> NotificationService:
    return NotificationService(db)

def get_notification_config_service(db: Session = Depends(get_db)) -> NotificationConfigService:
    return NotificationConfigService(db)

# --- Inyectores con Dependencias Circulares ---
# Definimos get_approval_service antes para poder usarlo en get_saas_service sin lambdas
def get_asset_service(
        db: Session = Depends(get_db),
        audit_service: AuditService = Depends(get_audit_service)
) -> AssetService:
    return AssetService(db=db, audit_service=audit_service, approval_service=None)

def get_manual_payment_service(db: Session = Depends(get_db), audit_service: AuditService = Depends(get_audit_service)) -> ManualPaymentService:
    return ManualPaymentService(db, approval_service=None, audit_service=audit_service)

def get_approval_service(
        db: Session = Depends(get_db),
        asset_service: AssetService = Depends(get_asset_service),
        manual_payment_service: ManualPaymentService = Depends(get_manual_payment_service)
) -> ApprovalService:
    approval_service = ApprovalService(db, asset_service=asset_service, manual_payment_service=manual_payment_service)
    asset_service.approval_service = approval_service
    manual_payment_service.approval_service = approval_service
    return approval_service

# ---------------------------------------------

def get_saas_service(
    db: Session = Depends(get_db),
    auth_service: AuthService = Depends(get_auth_service),
    approval_service: ApprovalService = Depends(get_approval_service), # CORRECCIÓN: Sin lambda
    notification_service: NotificationService = Depends(get_notification_service),
    audit_service: AuditService = Depends(get_audit_service)
) -> SaasService:
    saas_service = SaasService(
        db=db, 
        auth_service=auth_service, 
        approval_service=approval_service, 
        notification_service=notification_service,
        audit_service=audit_service
    )
    # Inyección para romper dependencia circular
    if approval_service:
        approval_service.saas_service = saas_service
    return saas_service


def get_usage_service(db: Session = Depends(get_db)) -> UsageService:
    return UsageService(db=db)


def get_partner_service(db: Session = Depends(get_db)) -> PartnerService:
    return PartnerService(db=db)

def get_marketing_service(db: Session = Depends(get_db)) -> MarketingService:
    return MarketingService(db=db)

def get_media_service(db: Session = Depends(get_db)) -> MediaService:
    return MediaService(db)


def get_alarming_service(
        db: Session = Depends(get_db),
        notification_service: NotificationService = Depends(get_notification_service),
        audit_service: AuditService = Depends(get_audit_service)
) -> AlarmingService:
    asset_repo = AssetRepository(db)
    return AlarmingService(db=db, notification_service=notification_service, asset_repo=asset_repo,
                           audit_service=audit_service)


def get_role_service(db: Session = Depends(get_db)) -> RoleService:
    return RoleService(db)


# --- Payment Services ---
def get_payment_service(db: Session = Depends(get_db)) -> PaymentService:
    return PaymentService(db)


def get_online_payment_service(db: Session = Depends(get_db)) -> OnlinePaymentService:
    return OnlinePaymentService(db)


# --- Procurement Services ---
def get_procurement_service(db: Session = Depends(get_db)) -> ProcurementService:
    return ProcurementService(db)


def get_evaluation_service(db: Session = Depends(get_db)) -> EvaluationService:
    return EvaluationService(db)

# --- Reporting Services ---
def get_reporting_service(db: Session = Depends(get_db)) -> ReportingService:
    return ReportingService(db=db)

def get_stoppage_service(db: Session = Depends(get_db)) -> StoppageService:
    return StoppageService(db=db)


# ---------------------------------------------

def get_telemetry_service(
        db: Session = Depends(get_db),
        audit_service: AuditService = Depends(get_audit_service)
) -> TelemetryService:
    return TelemetryService(db=db, audit_service=audit_service)


def get_maintenance_service(db: Session = Depends(get_db),
                            audit_service: AuditService = Depends(get_audit_service)) -> MaintenanceService:
    return MaintenanceService(db=db, audit_service=audit_service)


def get_core_engine_service(
        db: Session = Depends(get_db),
        telemetry_service: TelemetryService = Depends(get_telemetry_service),
        audit_service: AuditService = Depends(get_audit_service)
) -> CoreEngineService:
    return CoreEngineService(db=db, telemetry_service=telemetry_service, audit_service=audit_service)


def get_sector_service(db: Session = Depends(get_db),
                       audit_service: AuditService = Depends(get_audit_service)) -> SectorService:
    return SectorService(db=db, audit_service=audit_service)


def get_configuration_service(db: Session = Depends(get_db),
                              audit_service: AuditService = Depends(get_audit_service)) -> ConfigurationService:
    return ConfigurationService(db=db, audit_service=audit_service)


def get_limiter_key(request: Request) -> str:
    if 'tenant_id' in request.scope:
        return str(request.scope['tenant_id'])

    if request.client is not None and request.client.host is not None:
        return request.client.host

    return "test_fallback_key"
