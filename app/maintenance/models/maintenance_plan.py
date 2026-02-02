# /app/maintenance/models/maintenance_plan.py
"""
Modelo de la base de datos para la entidad MaintenancePlan.
"""
import uuid
from sqlalchemy import Column, String, Integer, ForeignKey, Boolean, TIMESTAMP, func
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from app.db.base_class import Base

class MaintenancePlan(Base):
    """
    Define una plantilla para generar Órdenes de Trabajo de forma proactiva.
    """
    __tablename__ = "maintenance_plans"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    
    name = Column(String(100), nullable=False, index=True)
    description = Column(String(255), nullable=True)
    
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id"), nullable=False, index=True)
    asset = relationship("Asset")
    
    # --- Plantilla para la Work Order ---
    summary_template = Column(String(255), nullable=False)
    category = Column(String(50), default="PREVENTIVE", nullable=False)
    priority = Column(String(50), default="MEDIUM", nullable=False)
    
    # --- Lógica del Disparador (Trigger) ---
    trigger_type = Column(String(50), default="TIME_BASED", nullable=False) # TIME_BASED, METER_BASED
    interval_days = Column(Integer, nullable=True, comment="Para TIME_BASED: ejecutar cada X días.")
    
    last_execution_at = Column(TIMESTAMP(timezone=True), nullable=True)
    is_active = Column(Boolean, default=True, nullable=False)
    
    # --- Relación Inversa ---
    tasks = relationship("MaintenancePlanTask", back_populates="plan", cascade="all, delete-orphan")
