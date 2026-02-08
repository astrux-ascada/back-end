# /app/identity/models/user.py
"""
Modelo de la base de datos para la entidad User.
"""
import uuid
from sqlalchemy import Boolean, Column, String, func, TIMESTAMP, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class User(Base):
    __tablename__ = "users"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=True)
    tenant = relationship("Tenant", foreign_keys=[tenant_id], back_populates="users")
    
    roles = relationship("Role", secondary="user_roles", back_populates="users")
    
    email = Column(String(100), unique=True, index=True, nullable=False)
    name = Column(String(100), nullable=True)
    hashed_password = Column(String(255), nullable=False)
    is_active = Column(Boolean(), default=True, nullable=False)
    
    tfa_secret = Column(String(255), nullable=True)
    is_tfa_enabled = Column(Boolean, default=False, nullable=False)

    created_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    updated_at = Column(TIMESTAMP(timezone=True), server_default=func.now(), onupdate=func.now(), nullable=False)
