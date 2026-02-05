# /app/dependencies/subscription.py
"""
Dependencias para la gestión de suscripciones, features y límites.
"""
import uuid
from fastapi import Depends, HTTPException, status, Request

from app.core.database import get_db
from sqlalchemy.orm import Session
from app.identity.models.saas import Subscription, Plan
from app.dependencies.tenant import get_tenant_id

# Lista blanca de rutas permitidas incluso con suscripción vencida
ALLOWED_ROUTES_PAST_DUE = [
    "/api/v1/saas/usage",
    "/api/v1/payments/history",
    "/api/v1/payments/checkout",
    # Se pueden añadir más rutas del portal de cliente aquí
]

def get_current_subscription(tenant_id: uuid.UUID = Depends(get_tenant_id), db: Session = Depends(get_db)) -> Subscription:
    subscription = db.query(Subscription).filter(Subscription.tenant_id == tenant_id).first()
    if not subscription:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No se encontró una suscripción para este tenant.")
    return subscription

def require_feature(feature_name: str):
    def _require_feature(subscription: Subscription = Depends(get_current_subscription)):
        plan_features = subscription.plan.features or {}
        if not plan_features.get(feature_name, False):
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail=f"La funcionalidad '{feature_name}' no está incluida en su plan actual ('{subscription.plan.name}')."
            )
    return _require_feature

def require_active_subscription(request: Request, subscription: Subscription = Depends(get_current_subscription)):
    """
    Verifica que la suscripción del tenant esté activa.
    Permite el acceso a rutas de facturación si el estado es 'PAST_DUE'.
    """
    if subscription.status == "ACTIVE":
        return # Todo en orden

    if subscription.status == "PAST_DUE":
        # Si la suscripción está vencida, solo permitir acceso a la lista blanca
        if request.url.path in ALLOWED_ROUTES_PAST_DUE:
            return
        else:
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail="Su suscripción ha vencido. Por favor, actualice su método de pago."
            )
    
    # Para cualquier otro estado inactivo (CANCELED, EXPIRED), denegar acceso.
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail=f"El acceso está denegado. El estado de su suscripción es: {subscription.status}"
    )
