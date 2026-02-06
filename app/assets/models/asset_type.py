# /app/assets/models/asset_type.py
"""
Modelo de la base de datos para la entidad AssetType.

Representa la plantilla o el "tipo" de un activo, no una instancia física.
Contiene la información reutilizable como el nombre, fabricante y modelo.
"""
import uuid

from sqlalchemy import Column, String, func, TIMESTAMP, ForeignKey, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class AssetType(Base):
    """Modelo SQLAlchemy para un Tipo de Activo (Catálogo)."""
    __tablename__ = "asset_types"
    __table_args__ = (
        UniqueConstraint('name', 'tenant_id', name='_name_tenant_uc'),
    )

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    tenant = relationship("Tenant")

    name = Column(String(100), index=True, nullable=False) # Ya no es unique por sí solo
    description = Column(String(255), nullable=True)
    manufacturer = Column(String(100), nullable=True)
    model_number = Column(String(100), nullable=True)
    category = Column(String(50), nullable=True, index=True)  # Ej: "Robot", "Sensor", "Motor"

    # Relación inversa: Un tipo de activo puede tener muchas instancias físicas.
    assets = relationship("Asset", back_populates="asset_type")

    # Relaciones para la jerarquía (Bill of Materials)
    parent_associations = relationship("AssetHierarchy", foreign_keys="[AssetHierarchy.child_asset_type_id]")
    child_associations = relationship("AssetHierarchy", foreign_keys="[AssetHierarchy.parent_asset_type_id]")

    # --- Campos de Auditoría ---
    created_at = Column(
        TIMESTAMP(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at = Column(
        TIMESTAMP(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )
