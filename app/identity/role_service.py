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

    def list_roles(self, tenant_id: uuid.UUID) -> List[Role]:
        """Devuelve una lista de todos los roles del tenant."""
        return self.role_repo.list_all(tenant_id)

    def list_permissions(self) -> List[Permission]:
        """Devuelve una lista de todos los permisos disponibles (Globales)."""
        return self.permission_repo.list_all()

    def get_role(self, role_id: uuid.UUID, tenant_id: uuid.UUID) -> Role:
        """Obtiene un rol por su ID, validando el tenant."""
        # Nota: get_by_id en repo no filtra por tenant, pero podemos validar después
        db_role = self.role_repo.get_by_id(role_id)
        if not db_role or db_role.tenant_id != tenant_id:
            raise NotFoundException("Rol no encontrado.")
        return db_role

    def create_role(self, role_in: RoleCreate, tenant_id: uuid.UUID) -> Role:
        """Crea un nuevo rol para el tenant, validando que el nombre no exista en ese tenant."""
        existing_role = self.role_repo.get_by_name(role_in.name, tenant_id)
        if existing_role:
            raise ConflictException(f"El rol con el nombre '{role_in.name}' ya existe en este tenant.")
        
        return self.role_repo.create(role_in, tenant_id)

    def update_role(self, role_id: uuid.UUID, role_in: RoleUpdate, tenant_id: uuid.UUID) -> Role:
        """Actualiza un rol existente del tenant."""
        db_role = self.get_role(role_id, tenant_id)

        if role_in.name and role_in.name != db_role.name:
            existing_role = self.role_repo.get_by_name(role_in.name, tenant_id)
            if existing_role:
                raise ConflictException(f"El rol con el nombre '{role_in.name}' ya existe en este tenant.")

        return self.role_repo.update(db_role=db_role, role_in=role_in)

    def delete_role(self, role_id: uuid.UUID, tenant_id: uuid.UUID) -> Role:
        """Elimina un rol del tenant."""
        db_role = self.get_role(role_id, tenant_id)
        # Aquí podrías añadir lógica para verificar si el rol está en uso antes de borrar.
        self.role_repo.delete(db_role=db_role)
        return db_role
