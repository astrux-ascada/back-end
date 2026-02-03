# /app/dependencies/subscription.py
"""
Dependencias de FastAPI relacionadas con la suscripción y los planes del tenant.
"""
import uuid
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.dependencies.database import get_db
from app.dependencies.tenant import get_tenant_id
from app.identity.models.saas.subscription import Subscription, SubscriptionStatus
from app.identity.models.saas.plan import Plan

def require_feature(feature_name: str):
    """
    Fábrica de dependencias que crea un validador para una feature específica del plan.

    Args:
        feature_name: El nombre de la clave en el JSON 'features' del plan.

    Returns:
        Una función de dependencia para ser usada en las rutas de FastAPI.
    """
    def _dependency(
        tenant_id: uuid.UUID = Depends(get_tenant_id),
        db: Session = Depends(get_db)
    ) -> None:
        """
        Valida si la feature requerida está habilitada para el plan del tenant actual.
        """
        # Buscar la suscripción activa del tenant
        subscription = (
            db.query(Subscription)
            .join(Plan)
            .filter(
                Subscription.tenant_id == tenant_id,
                Subscription.status.in_([SubscriptionStatus.ACTIVE, SubscriptionStatus.TRIAL])
            )
            .first()
        )

        if not subscription:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="No active subscription found for this tenant."
            )

        # Verificar si la feature está en el plan y es true
        plan_features = subscription.plan.features or {}
        if not plan_features.get(feature_name, False):
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail=f"Feature '{feature_name}' is not enabled for your current plan."
            )

    return _dependency
