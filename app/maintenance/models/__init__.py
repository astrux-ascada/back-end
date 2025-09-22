# /app/maintenance/models/__init__.py
"""
Expone los modelos del módulo de mantenimiento y define sus interrelaciones
para evitar dependencias circulares.
"""

from sqlalchemy.orm import relationship

# --- 1. Importar todas las clases de modelo necesarias ---

# Modelos de este módulo
from .work_order import WorkOrder
from .maintenance_task import MaintenanceTask
from .work_order_user_assignment import WorkOrderUserAssignment
from .work_order_provider_assignment import WorkOrderProviderAssignment

# Modelos de otros módulos con los que nos relacionamos
from app.identity.models.user import User
from app.procurement.models.provider import Provider


# --- 2. Definir las relaciones inversas (back-populates) ---
# Ahora que todas las clases están en el mismo ámbito, podemos crear los "puentes".

# Relación WorkOrder <-> MaintenanceTask
WorkOrder.tasks = relationship("MaintenanceTask", order_by=MaintenanceTask.order, back_populates="work_order")

# Relación WorkOrder <-> User (a través de la tabla de asignación)
WorkOrder.assigned_users = relationship("User", secondary="work_order_user_assignments", back_populates="work_orders")
User.work_orders = relationship("WorkOrder", secondary="work_order_user_assignments", back_populates="assigned_users")

# Relación WorkOrder <-> Provider (a través de la tabla de asignación)
WorkOrder.assigned_provider = relationship("Provider", secondary="work_order_provider_assignments", back_populates="work_orders")
Provider.work_orders = relationship("WorkOrder", secondary="work_order_provider_assignments", back_populates="assigned_provider")
