# Modelos relacionados con la estructura de la planta (Secciones, etc.)
import uuid
from sqlalchemy import (
    Column,
    String,
    Text,
)
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from app.core.db.base import Base


class Section(Base):
    __tablename__ = "sections"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4, index=True)
    name = Column(String(100), unique=True, nullable=False, index=True)
    description = Column(Text)

    # --- Relationships ---
    # Una sección tiene muchos activos
    assets = relationship("Asset", back_populates="section")

    # Una sección puede tener muchos usuarios, y un usuario muchas secciones
    users = relationship(
        "User", secondary="user_sections", back_populates="sections"
    )
