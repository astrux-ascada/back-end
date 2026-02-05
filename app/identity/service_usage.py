# /app/identity/service_usage.py
"""
Servicio para calcular y reportar el uso de recursos de un tenant.
"""
import uuid
from sqlalchemy.orm import Session

from app.identity.models import User
from app.assets.models import Asset
from app.identity.models.saas import Subscription, Plan
from app.identity.schemas_saas import UsageReport, UsageDetail
from app.core.exceptions import NotFoundException

class UsageService:
    def __init__(self, db: Session):
        self.db = db

    def get_usage_report(self, tenant_id: uuid.UUID) -> UsageReport:
        """
        Genera un reporte de uso de recursos para un tenant específico.
        """
        # 1. Obtener la suscripción y el plan del tenant
        subscription = self.db.query(Subscription).join(Plan).filter(Subscription.tenant_id == tenant_id).first()
        if not subscription or not subscription.plan:
            raise NotFoundException("No se encontró una suscripción activa para este tenant.")

        plan_limits = subscription.plan.limits

        # 2. Calcular el uso de usuarios
        user_count = self.db.query(User).filter(User.tenant_id == tenant_id).count()
        user_limit = plan_limits.get("max_users", -1)

        # 3. Calcular el uso de activos
        asset_count = self.db.query(Asset).filter(Asset.tenant_id == tenant_id).count()
        asset_limit = plan_limits.get("max_assets", -1)

        # 4. Construir el reporte
        report = UsageReport(
            users=UsageDetail(used=user_count, limit=user_limit),
            assets=UsageDetail(used=asset_count, limit=asset_limit)
        )

        return report
