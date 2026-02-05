# /app/payments/schemas.py
"""
Esquemas Pydantic para el módulo de Pagos.
"""
import uuid
from datetime import datetime
from typing import Optional, Dict, Any

from pydantic import BaseModel, Field
from .models import PaymentStatus, PaymentGateway, VoucherStatus

# --- Esquemas para PaymentTransaction ---

class PaymentTransactionBase(BaseModel):
    subscription_id: uuid.UUID
    amount: float
    currency: str = Field("USD", max_length=3)
    gateway: PaymentGateway
    gateway_transaction_id: Optional[str] = None
    payment_metadata: Optional[Dict[str, Any]] = None # Renombrado

class PaymentTransactionCreate(PaymentTransactionBase):
    pass

class ManualPaymentCreate(BaseModel):
    """Datos para solicitar un pago manual (transferencia/depósito)."""
    subscription_id: uuid.UUID
    amount: float
    reference_number: str = Field(..., min_length=4, description="Número de referencia de la transferencia.")
    evidence_file_id: uuid.UUID = Field(..., description="ID del archivo de comprobante subido.")
    notes: Optional[str] = None

class PaymentTransactionRead(PaymentTransactionBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    status: PaymentStatus
    reference_number: Optional[str]
    evidence_file_id: Optional[uuid.UUID]
    notes: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

# --- Esquemas para PaymentVoucher ---

class VoucherBase(BaseModel):
    code: str = Field(..., min_length=6, max_length=50)
    value: float
    currency: str = Field("USD", max_length=3)
    expires_at: Optional[datetime] = None

class VoucherCreate(VoucherBase):
    pass

class VoucherRead(VoucherBase):
    id: uuid.UUID
    status: VoucherStatus
    used_by_tenant_id: Optional[uuid.UUID] = None
    used_at: Optional[datetime] = None
    created_at: datetime

    class Config:
        from_attributes = True

class RedeemVoucherRequest(BaseModel):
    code: str = Field(..., description="El código del voucher a canjear.")
