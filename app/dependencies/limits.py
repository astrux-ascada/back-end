# /app/dependencies/limits.py
"""
Dependencias de FastAPI para verificar los límites cuantitativos del plan de un tenant.
"""
import uuid
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.dependencies.tenant import get_tenant_id
from app.identity.models import User, Role
from app.assets.models import Asset
from app.identity.models.saas import Subscription, Plan

def check_limit(entity_name: str):
    """
    Fábrica de dependencias que crea un validador para un límite específico del plan.

    Args:
        entity_name: El nombre de la entidad a verificar (ej: "users", "assets").
                     Debe coincidir con la clave en el JSON 'limits' del plan.

    Returns:
        Una función de dependencia para ser usada en los endpoints de creación.
    """
    def _dependency(
        tenant_id: uuid.UUID = Depends(get_tenant_id),
        db: Session = Depends(get_db)
    ) -> None:
        """
        Valida si el tenant ha alcanzado el límite para la entidad especificada.
        """
        # 1. Obtener la suscripción y el plan del tenant
        subscription = db.query(Subscription).join(Plan).filter(Subscription.tenant_id == tenant_id).first()
        if not subscription or not subscription.plan:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="No active subscription found.")

        # 2. Obtener el límite del plan
        limit_key = f"max_{entity_name}"
        limit_value = subscription.plan.limits.get(limit_key, -1) # -1 significa ilimitado

        if limit_value == -1:
            return # Límite ilimitado, no hay nada que verificar

        # 3. Contar las entidades existentes
        current_count = 0
        if entity_name == "users":
            current_count = db.query(User).filter(User.tenant_id == tenant_id).count()
        elif entity_name == "assets":
            current_count = db.query(Asset).filter(Asset.tenant_id == tenant_id).count()
        # Añadir otros casos para otras entidades...
        else:
            return # Si no sabemos cómo contar la entidad, lo permitimos por ahora

        # 4. Comparar y lanzar error si se excede
        if current_count >= limit_value:
            raise HTTPException(
                status_code=status.HTTP_402_PAYMENT_REQUIRED,
                detail=f"Límite de '{entity_name}' ({limit_value}) alcanzado. Por favor, actualice su plan."
            )

    return _dependency
