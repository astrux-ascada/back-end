# /app/payments/models.py
"""
Modelos de la base de datos para el módulo de Pagos.
"""
import uuid
import enum
from sqlalchemy import Column, String, Float, ForeignKey, DateTime, func, Enum, Text
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class PaymentStatus(str, enum.Enum):
    PENDING = "PENDING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"
    REFUNDED = "REFUNDED"
    AWAITING_APPROVAL = "AWAITING_APPROVAL"

class PaymentGateway(str, enum.Enum):
    STRIPE = "stripe"
    PAYPAL = "paypal"
    VOUCHER = "voucher"
    MANUAL = "manual"

class PaymentTransaction(Base):
    """
    Registra cada transacción de pago en el sistema.
    """
    __tablename__ = "payment_transactions"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    subscription_id = Column(UUID(as_uuid=True), ForeignKey("subscriptions.id"), nullable=False, index=True)
    
    amount = Column(Float, nullable=False)
    currency = Column(String(3), nullable=False, default="USD")
    
    status = Column(Enum(PaymentStatus), nullable=False, default=PaymentStatus.PENDING)
    gateway = Column(Enum(PaymentGateway), nullable=False)
    
    gateway_transaction_id = Column(String, nullable=True, index=True, comment="ID de la transacción en la pasarela externa.")
    
    # Renombrado de 'metadata' a 'payment_metadata' para evitar conflicto con SQLAlchemy
    payment_metadata = Column(JSONB, nullable=True, comment="Datos adicionales de la pasarela o del pago.")
    
    reference_number = Column(String, nullable=True, comment="Número de referencia bancaria o de depósito.")
    evidence_file_id = Column(UUID(as_uuid=True), nullable=True, comment="ID del archivo de comprobante en el Media Manager.")
    notes = Column(Text, nullable=True, comment="Notas del cliente o del administrador sobre este pago.")

    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(DateTime(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)

    tenant = relationship("Tenant")
    subscription = relationship("Subscription")


class VoucherStatus(str, enum.Enum):
    ACTIVE = "ACTIVE"
    USED = "USED"
    EXPIRED = "EXPIRED"

class PaymentVoucher(Base):
    """
    Representa un voucher o código de pago para canje offline.
    """
    __tablename__ = "payment_vouchers"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    code = Column(String, unique=True, nullable=False, index=True)
    
    value = Column(Float, nullable=False, comment="Valor monetario del voucher.")
    currency = Column(String(3), nullable=False, default="USD")
    
    status = Column(Enum(VoucherStatus), nullable=False, default=VoucherStatus.ACTIVE)
    expires_at = Column(DateTime(timezone=True), nullable=True)
    
    used_by_tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=True)
    used_at = Column(DateTime(timezone=True), nullable=True)
    
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)

    used_by_tenant = relationship("Tenant")
