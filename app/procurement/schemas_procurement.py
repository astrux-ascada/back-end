# /app/procurement/schemas_procurement.py
"""
Esquemas Pydantic para el flujo de Cotizaciones y Órdenes de Compra.
"""
import uuid
from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

from .models.purchase_order import RFQStatus, QuoteStatus, POStatus

# --- Esquemas para RequestForQuotation (RFQ) ---

class RFQBase(BaseModel):
    title: str
    description: Optional[str] = None
    work_order_id: Optional[uuid.UUID] = None
    deadline: Optional[datetime] = None

class RFQCreate(RFQBase):
    provider_ids: List[uuid.UUID] = Field(..., min_length=1, description="Lista de IDs de proveedores a invitar.")

class RFQRead(RFQBase):
    id: uuid.UUID
    status: RFQStatus
    created_at: datetime
    created_by_id: uuid.UUID

    class Config:
        from_attributes = True

# --- Esquemas para Quote ---

class QuoteBase(BaseModel):
    rfq_id: uuid.UUID
    provider_id: uuid.UUID
    total_price: float
    currency: str = "USD"
    delivery_days: Optional[int] = None

class QuoteCreate(QuoteBase):
    """Esquema para que un proveedor envíe una cotización."""
    pass

class QuoteRead(QuoteBase):
    id: uuid.UUID
    status: QuoteStatus
    submitted_at: datetime

    class Config:
        from_attributes = True

# --- Esquemas para PurchaseOrder (PO) ---

class POBase(BaseModel):
    quote_id: uuid.UUID

class POCreate(POBase):
    pass

class POReceive(BaseModel):
    """Esquema para registrar la recepción de una PO y evaluar al proveedor."""
    provider_rating: int = Field(..., ge=1, le=5, description="Calificación del proveedor para esta entrega (1-5).")
    provider_feedback: Optional[str] = Field(None, description="Comentarios sobre el desempeño del proveedor.")
    # Aquí se podrían añadir más campos, como la cantidad de items recibidos si fuera parcial.

class PORead(POBase):
    id: uuid.UUID
    status: POStatus
    issued_at: Optional[datetime]
    completed_at: Optional[datetime]
    provider_rating: Optional[int]
    provider_feedback: Optional[str]

    class Config:
        from_attributes = True

# --- Esquema para el Motor de Evaluación ---

class QuoteEvaluation(QuoteRead):
    """Extiende QuoteRead con datos de evaluación para la sugerencia."""
    provider_performance: float
    score: float
    justification: str

class RFQEvaluationReport(BaseModel):
    rfq: RFQRead
    quotes: List[QuoteEvaluation]
    recommended_quote_id: Optional[uuid.UUID] = None
