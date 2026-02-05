# /app/payments/service_online.py
"""
Servicio para gestionar pagos online (PayPal, Stripe).
"""
import uuid
from typing import Dict, Any
from sqlalchemy.orm import Session

from app.payments import models
from app.payments.gateways.paypal import PayPalGateway
from app.identity.models import User
from app.identity.models.saas import Plan
from app.core.exceptions import NotFoundException

class OnlinePaymentService:
    def __init__(self, db: Session):
        self.db = db
        # En el futuro, esto podría ser una fábrica que devuelve la pasarela correcta según la configuración
        self.gateway = PayPalGateway()

    async def create_checkout_session(self, plan_id: uuid.UUID, user: User, tenant_id: uuid.UUID, success_url: str, cancel_url: str) -> Dict[str, Any]:
        """
        Inicia el proceso de pago online para una suscripción.
        """
        plan = self.db.query(Plan).filter(Plan.id == plan_id).first()
        if not plan:
            raise NotFoundException("Plan no encontrado.")

        # Llamar a la pasarela para obtener la URL de pago
        session_data = await self.gateway.create_checkout_session(user, plan, success_url, cancel_url)
        
        # Registrar la transacción como PENDIENTE
        # Nota: En un flujo real, esto se confirmaría vía Webhook
        db_transaction = models.PaymentTransaction(
            tenant_id=tenant_id,
            subscription_id=uuid.uuid4(), # Placeholder, se debería crear o buscar la suscripción real
            amount=plan.price_monthly,
            currency=plan.currency,
            gateway=models.PaymentGateway.PAYPAL,
            status=models.PaymentStatus.PENDING,
            gateway_transaction_id=session_data.get("order_id")
        )
        # self.db.add(db_transaction) # Comentado porque necesitamos una suscripción válida
        # self.db.commit()

        return session_data
