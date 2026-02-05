# /app/core_engine/models/data_source.py
import uuid
from sqlalchemy import Column, String, Boolean, ForeignKey
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.db.base_class import Base

class DataSource(Base):
    __tablename__ = "data_sources"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    # Aislamiento por Tenant
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    
    name = Column(String, nullable=False, index=True)
    protocol = Column(String, nullable=False, index=True) # e.g., "modbus_tcp", "opc_ua"
    
    # Parámetros de conexión específicos del protocolo
    connection_params = Column(JSONB, nullable=False)
    
    is_active = Column(Boolean, default=True, index=True)

    tenant = relationship("Tenant")
