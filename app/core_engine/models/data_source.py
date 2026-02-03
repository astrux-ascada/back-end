# /app/core_engine/models/data_source.py
import uuid
from sqlalchemy import Column, String, Boolean
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base

class DataSource(Base):
    __tablename__ = "data_sources"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, index=True)
    protocol = Column(String, nullable=False, index=True)
    is_active = Column(Boolean, default=True, index=True)
