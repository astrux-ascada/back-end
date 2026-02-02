# /app/identity/role_service.py
"""
Servicio de negocio para la gestión de Roles y Permisos.
"""

import logging
import uuid
from typing import List, Optional

from sqlalchemy.orm import Session

from app.core.exceptions import NotFoundException, ConflictException
from app.identity.models import Role, Permission
from app.identity.repository import RoleRepository, PermissionRepository
from app.identity.schemas import RoleCreate, RoleUpdate

logger = logging.getLogger(__name__)

class RoleService:
    """Servicio de negocio para la gestión de roles y sus permisos."""

    def __init__(self, db: Session):
        self.db = db
        self.role_repo = RoleRepository(db)
        self.permission_repo = PermissionRepository(db)

    def list_roles(self) -> List[Role]:
        """Devuelve una lista de todos los roles."""
        return self.role_repo.list_all()

    def list_permissions(self) -> List[Permission]:
        """Devuelve una lista de todos los permisos disponibles."""
        return self.permission_repo.list_all()

    def get_role(self, role_id: uuid.UUID) -> Role:
        """Obtiene un rol por su ID."""
        db_role = self.role_repo.get_by_id(role_id)
        if not db_role:
            raise NotFoundException("Rol no encontrado.")
        return db_role

    def create_role(self, role_in: RoleCreate) -> Role:
        """Crea un nuevo rol, validando que el nombre no exista."""
        existing_role = self.role_repo.get_by_name(role_in.name)
        if existing_role:
            raise ConflictException(f"El rol con el nombre '{role_in.name}' ya existe.")
        
        return self.role_repo.create(role_in)

    def update_role(self, role_id: uuid.UUID, role_in: RoleUpdate) -> Role:
        """Actualiza un rol existente."""
        db_role = self.get_role(role_id)

        if role_in.name and role_in.name != db_role.name:
            existing_role = self.role_repo.get_by_name(role_in.name)
            if existing_role:
                raise ConflictException(f"El rol con el nombre '{role_in.name}' ya existe.")

        return self.role_repo.update(db_role=db_role, role_in=role_in)

    def delete_role(self, role_id: uuid.UUID):
        """Elimina un rol."""
        db_role = self.get_role(role_id)
        # Aquí podrías añadir lógica para verificar si el rol está en uso antes de borrar.
        self.role_repo.delete(db_role=db_role)
