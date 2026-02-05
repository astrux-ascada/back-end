# /app/payments/api.py
"""
API Router para el módulo de Pagos.
"""
import logging
import uuid
from typing import List, Dict, Any

from fastapi import APIRouter, Depends, status, HTTPException, Body

from app.payments import schemas
from app.payments.service_manual import ManualPaymentService
from app.payments.service_online import OnlinePaymentService
from app.dependencies.services import get_manual_payment_service, get_online_payment_service
from app.dependencies.tenant import get_tenant_id
from app.dependencies.auth import get_current_active_user
from app.identity.models import User

logger = logging.getLogger("app.payments.api")

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/manual", response_model=schemas.PaymentTransactionRead, status_code=status.HTTP_201_CREATED)
def request_manual_payment(
    payment_in: schemas.ManualPaymentCreate,
    payment_service: ManualPaymentService = Depends(get_manual_payment_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
    current_user: User = Depends(get_current_active_user)
):
    """
    Solicita un pago manual (transferencia/depósito).
    Crea una transacción pendiente y una solicitud de aprobación para el administrador.
    """
    return payment_service.create_payment_request(payment_in, current_user, tenant_id)

@router.post("/checkout", status_code=status.HTTP_200_OK)
async def create_checkout_session(
    plan_id: uuid.UUID = Body(..., embed=True),
    success_url: str = Body(..., embed=True),
    cancel_url: str = Body(..., embed=True),
    payment_service: OnlinePaymentService = Depends(get_online_payment_service),
    tenant_id: uuid.UUID = Depends(get_tenant_id),
    current_user: User = Depends(get_current_active_user)
) -> Dict[str, Any]:
    """
    Inicia una sesión de pago online (PayPal).
    Devuelve la URL de aprobación para redirigir al usuario.
    """
    return await payment_service.create_checkout_session(plan_id, current_user, tenant_id, success_url, cancel_url)
