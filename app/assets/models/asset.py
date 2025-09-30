# /app/assets/models/asset.py
"""
Modelo de la base de datos para la entidad Asset.

Representa una instancia física y única de un activo en la planta.
"""
import uuid

from sqlalchemy import Column, String, func, TIMESTAMP, ForeignKey, Date
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class Asset(Base):
    """Modelo SQLAlchemy para una Instancia de Activo Físico."""
    __tablename__ = "assets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)

    # --- Relaciones ---
    asset_type_id = Column(UUID(as_uuid=True), ForeignKey("asset_types.id"), nullable=False)
    asset_type = relationship("AssetType", back_populates="assets")

    sector_id = Column(UUID(as_uuid=True), ForeignKey("sectors.id"), nullable=True, index=True)
    sector = relationship("Sector", back_populates="assets")

    # --- Campos de Instancia Única ---
    serial_number = Column(String(100), unique=True, nullable=True, index=True)
    location = Column(String(150), nullable=True)  # Ej: "Línea 3, Estación 2"
    status = Column(String(50), default="operational", nullable=False, index=True) # Ej: "operational", "maintenance", "failed"
    
    # --- MEJORA: Campo flexible para propiedades específicas del activo ---
    properties = Column(JSONB, nullable=True, comment="Propiedades específicas del activo en formato JSON.")

    # --- Fechas Clave del Ciclo de Vida ---
    installed_at = Column(Date, nullable=True)
    last_maintenance_at = Column(Date, nullable=True)
    warranty_expires_at = Column(Date, nullable=True)

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
