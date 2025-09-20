
from sqlalchemy import (
    Column,
    Integer,
    String,
    Double,
    DateTime,
    ForeignKey,
    PrimaryKeyConstraint,
)
from sqlalchemy.orm import relationship

from app.core.db.base import Base


class SensorData(Base):
    __tablename__ = "sensor_data"

    time = Column(DateTime(timezone=True), nullable=False)
    sensor_id = Column(Integer, ForeignKey("assets.id", ondelete="CASCADE"), nullable=False)
    value = Column(Double, nullable=False)
    unit = Column(String(50))
    quality = Column(String(20), default="good")

    # --- Relaciones ---
    sensor = relationship("Asset", back_populates="sensor_data")

    # --- Constraints ---
    # TimescaleDB requiere una clave primaria que incluya la columna de tiempo.
    __table_args__ = (PrimaryKeyConstraint("time", "sensor_id"),)
