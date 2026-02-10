# /app/identity/repository.py
"""
Capa de Repositorio para el módulo de Identidad (User, Role, Permission).
"""

import uuid
from typing import List, Optional
from sqlalchemy.orm import Session, joinedload
from sqlalchemy import and_, not_ # Importar not_

from app.core.config import settings
from app.core.security import hash_password
from app.identity.models import User, Role, Permission
from app.identity.schemas import UserCreate, RoleCreate, UserUpdate, RoleUpdate
from app.sectors.repository import SectorRepository


class PermissionRepository:
    """Realiza operaciones CRUD para el modelo Permission."""
    def __init__(self, db: Session):
        self.db = db

    def list_all(self) -> List[Permission]:
        return self.db.query(Permission).all()

    def get_by_ids(self, permission_ids: List[uuid.UUID]) -> List[Permission]:
        return self.db.query(Permission).filter(Permission.id.in_(permission_ids)).all()


class RoleRepository:
    """Realiza operaciones CRUD para el modelo Role."""
    def __init__(self, db: Session):
        self.db = db
        self.permission_repo = PermissionRepository(db)

    def get_by_id(self, role_id: uuid.UUID) -> Optional[Role]:
        return self.db.query(Role).options(joinedload(Role.permissions)).filter(Role.id == role_id).first()

    def get_by_name(self, name: str, tenant_id: uuid.UUID) -> Optional[Role]:
        # Los roles también deberían ser por tenant
        return self.db.query(Role).filter(Role.name == name, Role.tenant_id == tenant_id).first()

    def list_all(self, tenant_id: uuid.UUID) -> List[Role]:
        return self.db.query(Role).filter(Role.tenant_id == tenant_id).options(joinedload(Role.permissions)).all()

    def get_by_ids(self, role_ids: List[uuid.UUID]) -> List[Role]:
        return self.db.query(Role).filter(Role.id.in_(role_ids)).all()

    def create(self, role_in: RoleCreate, tenant_id: uuid.UUID) -> Role:
        role_data = role_in.model_dump(exclude={"permission_ids"})
        db_role = Role(**role_data, tenant_id=tenant_id)

        if role_in.permission_ids:
            permissions = self.permission_repo.get_by_ids(role_in.permission_ids)
            db_role.permissions = permissions

        self.db.add(db_role)
        self.db.commit()
        self.db.refresh(db_role)
        return db_role

    def update(self, db_role: Role, role_in: RoleUpdate) -> Role:
        update_data = role_in.model_dump(exclude_unset=True)
        
        for field, value in update_data.items():
            if field != "permission_ids":
                setattr(db_role, field, value)

        if role_in.permission_ids is not None:
            permissions = self.permission_repo.get_by_ids(role_in.permission_ids)
            db_role.permissions = permissions

        self.db.add(db_role)
        self.db.commit()
        self.db.refresh(db_role)
        return db_role

    def delete(self, db_role: Role):
        self.db.delete(db_role)
        self.db.commit()


class UserRepository:
    """Realiza operaciones CRUD para el modelo User."""
    def __init__(self, db: Session):
        self.db = db
        self.role_repo = RoleRepository(db)
        self.sector_repo = SectorRepository(db)

    def get_by_id(self, user_id: uuid.UUID) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_id_and_tenant(self, user_id: uuid.UUID, tenant_id: uuid.UUID) -> User | None:
        return self.db.query(User).filter(User.id == user_id, User.tenant_id == tenant_id).first()

    def get_by_email(self, email: str) -> User | None:
        # El email es único en toda la plataforma, no necesita filtro de tenant
        return self.db.query(User).filter(User.email == email).first()

    def list_users(self, tenant_id: uuid.UUID, skip: int, limit: int) -> List[User]:
        """Devuelve una lista de usuarios para un tenant específico."""
        return self.db.query(User).filter(User.tenant_id == tenant_id).offset(skip).limit(limit).all()

    def list_all_users(self, exclude_super_admins: bool = False, skip: int = 0, limit: int = 100) -> List[User]:
        """
        Devuelve una lista de todos los usuarios de la plataforma.
        Opcionalmente puede excluir a los super administradores.
        """
        query = self.db.query(User)
        if exclude_super_admins:
            # Subconsulta para encontrar los IDs de los super admins
            # Usamos .subquery() para que pueda ser referenciada en el .in_()
            super_admin_role_ids = self.db.query(Role.id).filter(Role.name == settings.SUPER_ADMIN_ROLE_NAME).subquery()
            
            # Filtra los usuarios que NO tienen el rol de super admin
            query = query.filter(
                not_(User.roles.any(Role.id.in_(super_admin_role_ids)))
            )
            
        return query.offset(skip).limit(limit).all()

    def create(self, user_in: UserCreate, tenant_id: Optional[uuid.UUID] = None) -> User:
        user_data = user_in.model_dump(exclude={"password", "role_ids", "sector_ids"})
        user_data["hashed_password"] = hash_password(user_in.password)
        db_user = User(**user_data, tenant_id=tenant_id)

        if user_in.role_ids:
            roles = self.role_repo.get_by_ids(user_in.role_ids)
            db_user.roles = roles

        if user_in.sector_ids:
            sectors = self.sector_repo.get_by_ids(user_in.sector_ids)
            db_user.assigned_sectors = sectors

        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def update(self, db_user: User, user_in: UserUpdate) -> User:
        update_data = user_in.model_dump(exclude_unset=True)

        for field, value in update_data.items():
            if field not in ["role_ids", "sector_ids"]:
                setattr(db_user, field, value)

        if user_in.role_ids is not None:
            roles = self.role_repo.get_by_ids(user_in.role_ids)
            db_user.roles = roles

        if user_in.sector_ids is not None:
            sectors = self.sector_repo.get_by_ids(user_in.sector_ids)
            db_user.assigned_sectors = sectors

        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user

    def soft_delete(self, db_user: User) -> User:
        db_user.is_active = False
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
