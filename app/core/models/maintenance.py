
import enum
from sqlalchemy import (
    Column,
    Integer,
    String,
    Text,
    ForeignKey,
    DateTime,
    Enum,
    func,
)
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import relationship

from app.core.db.base import Base


class MaintenancePriority(enum.Enum):
    low = "low"
    medium = "medium"
    high = "high"
    critical = "critical"


class MaintenanceStatus(enum.Enum):
    pending = "pending"
    in_progress = "in_progress"
    on_hold = "on_hold"
    completed = "completed"
    cancelled = "cancelled"


class MaintenanceOrder(Base):
    __tablename__ = "maintenance_orders"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text)

    priority = Column(
        Enum(MaintenancePriority, name="maintenance_priority_enum"),
        nullable=False,
        default=MaintenancePriority.medium,
    )
    status = Column(
        Enum(MaintenanceStatus, name="maintenance_status_enum"),
        nullable=False,
        default=MaintenanceStatus.pending,
        index=True,
    )

    due_date = Column(DateTime(timezone=True), index=True)
    completed_at = Column(DateTime(timezone=True))
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    # --- Foreign Keys ---
    asset_id = Column(Integer, ForeignKey("assets.id"), nullable=False)
    assigned_to_id = Column(Integer, ForeignKey("users.id"))

    # --- JSON Fields ---
    checklist = Column(JSONB)  # e.g., [{"step": "Check pressure", "completed": false}]
    evidence = Column(JSONB)   # e.g., {"before_photos": [...], "after_notes": "..."}

    # --- Relationships ---
    asset = relationship("Asset", back_populates="maintenance_orders")
    assigned_to = relationship("User", back_populates="maintenance_orders")


class SparePart(Base):
    __tablename__ = "spare_parts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(200), nullable=False)
    code = Column(String(50), unique=True, nullable=False, index=True)
    category = Column(String(100))

    location = Column(Text)  # e.g., "Warehouse A, Shelf 3, Bin 7"

    stock_level = Column(Integer, nullable=False, default=0, index=True)
    min_level = Column(Integer, nullable=False, default=5)

    avg_monthly_usage = Column(Integer, default=0)
    last_used = Column(DateTime(timezone=True))
