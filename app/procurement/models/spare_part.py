# /app/procurement/models/spare_part.py
import uuid
from sqlalchemy import Column, String, Integer, Float
from sqlalchemy.dialects.postgresql import UUID

from app.db.base_class import Base

class SparePart(Base):
    __tablename__ = "spare_parts"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, index=True)
    part_number = Column(String, unique=True, index=True)
    stock_quantity = Column(Integer, default=0)
    price = Column(Float, default=0.0)
