# /app/identity/models/saas/partner.py
"""
Modelo para los Operadores Regionales (Partners) de Astruxa.
"""
import uuid
from sqlalchemy import Column, String, Float, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class Partner(Base):
    __tablename__ = "partners"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False)
    code = Column(String(20), unique=True, index=True, nullable=False)
    commission_rate = Column(Float, nullable=False, default=0.0)
    
    tenants = relationship("Tenant", back_populates="partner")

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
