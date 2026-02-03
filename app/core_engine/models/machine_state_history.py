# /app/core_engine/models/machine_state_history.py
import uuid
from sqlalchemy import Column, String, DateTime, ForeignKey, func
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base

class MachineStateHistory(Base):
    __tablename__ = "machine_state_history"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    asset_id = Column(UUID(as_uuid=True), ForeignKey("assets.id"), nullable=False, index=True)
    state = Column(String, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
