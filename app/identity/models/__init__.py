# /app/identity/models/__init__.py
"""
Expone los modelos del módulo de identidad y define sus interrelaciones
para evitar dependencias circulares.
"""

from sqlalchemy.orm import relationship

# --- 1. Importar todas las clases de modelo necesarias ---

# Modelos de este módulo
from .user import User
from .role import Role
from .permission import Permission
from .role_permission_association import RolePermissionAssociation
from .user_role_association import UserRoleAssociation
from .user_sector_association import UserSectorAssociation

# Modelos SaaS (Multi-Tenancy)
from .saas.partner import Partner
from .saas.plan import Plan
from .saas.tenant import Tenant
from .saas.subscription import Subscription

# Modelos de otros módulos con los que nos relacionamos
from app.sectors.models.sector import Sector


# --- 2. Definir las relaciones inversas (back-populates) ---
# Ahora que todas las clases están en el mismo ámbito, podemos crear los "puentes".

# Relación User <-> Sector
User.assigned_sectors = relationship("Sector", secondary="user_sectors", back_populates="users")
Sector.users = relationship("User", secondary="user_sectors", back_populates="assigned_sectors")
