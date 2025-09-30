# /app/identity/models/__init__.py
"""
Este archivo convierte el directorio 'models' en un paquete de Python
y expone todos los modelos del módulo de identidad para facilitar las importaciones
y asegurar que Alembic los descubra.
"""

from .user import User
from .role import Role
from .permission import Permission
from .role_permission_association import RolePermissionAssociation
from .user_role_association import UserRoleAssociation
from .user_sector_association import UserSectorAssociation
