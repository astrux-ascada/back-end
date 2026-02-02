# /app/core_engine/models/machine_state_history.py
"""
Modelo de la base de datos para el historial de estados operacionales de las máquinas.
"""
import uuid
from sqlalchemy import Column, String, TIMESTAMP, ForeignKey, Float
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.db.base_class import Base


class MachineStateHistory(Base):
    __tablename__ = "machine_state_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id"), nullable=False, index=True)
    
    state = Column(String, nullable=False)  # e.g., 'RUNNING', 'STOPPED', 'IDLE'
    
    start_time = Column(TIMESTAMP(timezone=True), server_default=func.now(), nullable=False)
    end_time = Column(TIMESTAMP(timezone=True), nullable=True) # Null for current state
    
    duration_seconds = Column(Float, nullable=True) # Calculated duration

    asset = relationship("Asset")
