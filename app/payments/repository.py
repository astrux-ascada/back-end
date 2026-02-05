# /app/payments/repository.py
"""
Capa de Repositorio para el módulo de Pagos.
"""
from typing import List, Optional
import uuid
from sqlalchemy.orm import Session

from app.payments import models, schemas

class PaymentRepository:
    def __init__(self, db: Session):
        self.db = db

    def create_transaction(self, transaction: models.PaymentTransaction) -> models.PaymentTransaction:
        self.db.add(transaction)
        self.db.commit()
        self.db.refresh(transaction)
        return transaction

    def get_transaction(self, transaction_id: uuid.UUID, tenant_id: uuid.UUID) -> Optional[models.PaymentTransaction]:
        return self.db.query(models.PaymentTransaction).filter(
            models.PaymentTransaction.id == transaction_id,
            models.PaymentTransaction.tenant_id == tenant_id
        ).first()

    def list_transactions(self, tenant_id: uuid.UUID, skip: int = 0, limit: int = 100) -> List[models.PaymentTransaction]:
        return self.db.query(models.PaymentTransaction).filter(
            models.PaymentTransaction.tenant_id == tenant_id
        ).order_by(models.PaymentTransaction.created_at.desc()).offset(skip).limit(limit).all()
