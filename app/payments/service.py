# /app/payments/service.py
"""
Servicio general para operaciones de lectura y gestión de pagos.
"""
import uuid
from typing import List
from sqlalchemy.orm import Session

from app.payments import models
from app.payments.repository import PaymentRepository

class PaymentService:
    def __init__(self, db: Session):
        self.db = db
        self.payment_repo = PaymentRepository(db)

    def list_transactions(self, tenant_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[models.PaymentTransaction]:
        """
        Lista el historial de transacciones de pago de un tenant.
        """
        return self.payment_repo.list_transactions(tenant_id, skip, limit)
