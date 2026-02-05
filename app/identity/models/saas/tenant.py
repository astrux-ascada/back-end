# /app/identity/models/saas/tenant.py
"""
Modelo para las Organizaciones (Clientes Finales) de Astruxa.
"""
import uuid
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String(100), nullable=False, index=True)
    slug = Column(String(100), unique=True, index=True, nullable=False)
    
    partner_id = Column(UUID(as_uuid=True), ForeignKey("partners.id"), nullable=True)
    partner = relationship("Partner", back_populates="tenants")
    
    subscription = relationship("Subscription", uselist=False, back_populates="tenant")
    users = relationship("User", back_populates="tenant")
