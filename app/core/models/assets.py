
import uuid
from sqlalchemy import (
    Column,
    String,
    Text,
    Float,
    DateTime,
    Table,
    ForeignKey,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB, UUID
from sqlalchemy.orm import relationship

from app.core.db.base import Base

# Tabla de asociación para la jerarquía de activos (relación muchos a muchos)
asset_hierarchy = Table(
    "asset_hierarchy",
    Base.metadata,
    Column("parent_asset_id", UUID(as_uuid=True), ForeignKey("assets.id", ondelete="CASCADE"), primary_key=True),
    Column("child_asset_id", UUID(as_uuid=True), ForeignKey("assets.id", ondelete="CASCADE"), primary_key=True),
)

class Asset(Base):
    __tablename__ = "assets"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(200), nullable=False)
    code = Column(String(50), unique=True, nullable=False, index=True)
    type = Column(String(50), nullable=False, index=True)  # e.g., 'machine', 'sensor', 'line'
    location = Column(Text)
    status = Column(String(50), default="unknown", index=True)
    health_score = Column(Float, default=100.0)
    asset_metadata = Column(JSONB)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # --- Foreign Keys ---
    section_id = Column(UUID(as_uuid=True), ForeignKey("sections.id"), nullable=False)

    # --- Relaciones ---
    # Relación con la sección (muchos a uno)
    section = relationship("Section", back_populates="assets")

    # Jerarquía padre-hijo (muchos a muchos, autorreferenciada)
    parents = relationship(
        "Asset",
        secondary=asset_hierarchy,
        primaryjoin=id == asset_hierarchy.c.child_asset_id,
        secondaryjoin=id == asset_hierarchy.c.parent_asset_id,
        back_populates="children",
    )
    children = relationship(
        "Asset",
        secondary=asset_hierarchy,
        primaryjoin=id == asset_hierarchy.c.parent_asset_id,
        secondaryjoin=id == asset_hierarchy.c.child_asset_id,
        back_populates="parents",
        cascade="all, delete"
    )

    # Órdenes de mantenimiento (uno a muchos)
    maintenance_orders = relationship("MaintenanceOrder", back_populates="asset", cascade="all, delete")

    # Datos de sensores (uno a muchos)
    sensor_data = relationship("SensorData", back_populates="sensor", cascade="all, delete")
