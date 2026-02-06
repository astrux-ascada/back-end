# /app/procurement/models/purchase_order.py
"""
Modelos de la base de datos para el flujo de Cotizaciones y Órdenes de Compra.
"""
import uuid
import enum
from sqlalchemy import Column, String, Float, ForeignKey, DateTime, func, Enum, Text, Integer
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class RFQStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    SENT = "SENT"
    CLOSED = "CLOSED"
    CANCELLED = "CANCELLED"

class QuoteStatus(str, enum.Enum):
    SUBMITTED = "SUBMITTED"
    ACCEPTED = "ACCEPTED"
    REJECTED = "REJECTED"

class POStatus(str, enum.Enum):
    DRAFT = "DRAFT"
    ISSUED = "ISSUED" # Enviada al proveedor
    COMPLETED = "COMPLETED" # Recibida
    CANCELLED = "CANCELLED"

class RequestForQuotation(Base):
    """Solicitud de Cotización (RFQ) para repuestos o servicios."""
    __tablename__ = "rfqs"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    work_order_id = Column(UUID(as_uuid=True), ForeignKey("work_orders.id"), nullable=True, index=True)
    
    title = Column(String, nullable=False)
    description = Column(Text)
    status = Column(Enum(RFQStatus), default=RFQStatus.DRAFT, nullable=False)
    
    created_by_id = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    deadline = Column(DateTime(timezone=True)) # Fecha límite para recibir cotizaciones

    quotes = relationship("Quote", back_populates="rfq")
    created_by = relationship("User")

class Quote(Base):
    """Cotización enviada por un proveedor en respuesta a una RFQ."""
    __tablename__ = "quotes"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    rfq_id = Column(UUID(as_uuid=True), ForeignKey("rfqs.id"), nullable=False, index=True)
    provider_id = Column(UUID(as_uuid=True), ForeignKey("providers.id"), nullable=False, index=True)
    
    total_price = Column(Float, nullable=False)
    currency = Column(String(3), default="USD", nullable=False)
    delivery_days = Column(Integer, nullable=True)
    status = Column(Enum(QuoteStatus), default=QuoteStatus.SUBMITTED, nullable=False)
    
    submitted_at = Column(DateTime(timezone=True), server_default=func.now())
    
    rfq = relationship("RequestForQuotation", back_populates="quotes")
    provider = relationship("Provider")

class PurchaseOrder(Base):
    """Orden de Compra generada a partir de una cotización aceptada."""
    __tablename__ = "purchase_orders"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    quote_id = Column(UUID(as_uuid=True), ForeignKey("quotes.id"), nullable=False, unique=True)
    
    status = Column(Enum(POStatus), default=POStatus.DRAFT, nullable=False)
    
    issued_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))

    # --- Campos de Evaluación del Proveedor (IA Feedback Loop) ---
    provider_rating = Column(Integer, nullable=True, comment="Calificación del proveedor para esta entrega (1-5).")
    provider_feedback = Column(Text, nullable=True, comment="Comentarios sobre el desempeño del proveedor.")
    
    quote = relationship("Quote", backref="purchase_order")
