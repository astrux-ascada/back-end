# /app/payments/service_manual.py
"""
Servicio para gestionar el flujo de pagos manuales (transferencias, depósitos).
"""
import uuid
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.payments import models, schemas
from app.auditing.approval_service import ApprovalService
from app.auditing.schemas import ApprovalRequestCreate
from app.auditing.service import AuditService # Importar AuditService
from app.identity.models import User
from app.core.exceptions import NotFoundException

class ManualPaymentService:
    def __init__(self, db: Session, approval_service: ApprovalService, audit_service: AuditService):
        self.db = db
        self.approval_service = approval_service
        self.audit_service = audit_service

    def create_payment_request(self, payment_in: schemas.ManualPaymentCreate, user: User, tenant_id: uuid.UUID) -> models.PaymentTransaction:
        """
        Crea una transacción de pago manual y una solicitud de aprobación.
        """
        # 1. Crear la transacción de pago en estado 'AWAITING_APPROVAL'
        db_transaction = models.PaymentTransaction(
            tenant_id=tenant_id,
            subscription_id=payment_in.subscription_id,
            amount=payment_in.amount,
            gateway=models.PaymentGateway.MANUAL,
            status=models.PaymentStatus.AWAITING_APPROVAL,
            reference_number=payment_in.reference_number,
            evidence_file_id=payment_in.evidence_file_id,
            notes=payment_in.notes
        )
        self.db.add(db_transaction)
        self.db.flush() # Para obtener el ID de la transacción

        # 2. Crear la solicitud de aprobación
        approval_request_in = ApprovalRequestCreate(
            entity_type="PAYMENT_TRANSACTION",
            entity_id=db_transaction.id,
            action="APPROVE_MANUAL_PAYMENT",
            request_justification=f"Solicitud de aprobación para pago manual de {payment_in.amount} {db_transaction.currency}.",
            payload=payment_in.model_dump()
        )
        self.approval_service.create_request(approval_request_in, user, tenant_id)
        
        self.db.commit()
        self.db.refresh(db_transaction)
        return db_transaction

    def _execute_approve_payment(self, transaction_id: uuid.UUID, approver: User):
        """
        (Método interno) Ejecuta la aprobación del pago.
        Llamado por el ApprovalService.
        """
        transaction = self.db.query(models.PaymentTransaction).filter(models.PaymentTransaction.id == transaction_id).first()
        if not transaction:
            raise NotFoundException("Transacción de pago no encontrada.")

        # 1. Marcar la transacción como completada
        transaction.status = models.PaymentStatus.COMPLETED
        
        # 2. Extender la suscripción (ej: añadir 30 días)
        subscription = transaction.subscription
        if subscription:
            # Lógica simple: extender 30 días desde el fin del periodo actual o desde hoy si ya expiró
            start_date = max(subscription.current_period_end, datetime.utcnow())
            subscription.current_period_end = start_date + timedelta(days=30)
            self.db.add(subscription)
            
        self.db.add(transaction)
        self.db.commit()

        # 3. Registrar en la auditoría
        self.audit_service.log_operation(user=approver, action="EXECUTE_APPROVE_PAYMENT", entity=transaction)
