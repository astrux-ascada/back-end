# /app/identity/repository.py
"""
Capa de Repositorio para el módulo de Identidad (User, Role, Permission).
"""

import uuid
from typing import List
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.identity.models import User, Role, Permission
from app.identity.schemas import UserCreate, RoleCreate
from app.sectors.repository import SectorRepository


class PermissionRepository:
    """Realiza operaciones CRUD para el modelo Permission."""
    def __init__(self, db: Session):
        self.db = db

    def get_by_ids(self, permission_ids: List[uuid.UUID]) -> List[Permission]:
        return self.db.query(Permission).filter(Permission.id.in_(permission_ids)).all()


class RoleRepository:
    """Realiza operaciones CRUD para el modelo Role."""
    def __init__(self, db: Session):
        self.db = db
        self.permission_repo = PermissionRepository(db)

    def get_by_ids(self, role_ids: List[uuid.UUID]) -> List[Role]:
        return self.db.query(Role).filter(Role.id.in_(role_ids)).all()

    def create(self, role_in: RoleCreate) -> Role:
        role_data = role_in.model_dump(exclude={"permission_ids"})
        db_role = Role(**role_data)

        if role_in.permission_ids:
            permissions = self.permission_repo.get_by_ids(role_in.permission_ids)
            db_role.permissions = permissions

        self.db.add(db_role)
        self.db.commit()
        self.db.refresh(db_role)
        return db_role


class UserRepository:
    """Realiza operaciones CRUD para el modelo User."""
    def __init__(self, db: Session):
        self.db = db
        self.role_repo = RoleRepository(db)
        self.sector_repo = SectorRepository(db)

    def get_by_id(self, user_id: uuid.UUID) -> User | None:
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> User | None:
        return self.db.query(User).filter(User.email == email).first()

    def create(self, user_in: UserCreate) -> User:
        """
        Crea un nuevo usuario, asignando sus roles y sectores.
        """
        user_data = user_in.model_dump(exclude={"password", "role_ids", "sector_ids"})
        user_data["hashed_password"] = hash_password(user_in.password)

        db_user = User(**user_data)

        if user_in.role_ids:
            roles = self.role_repo.get_by_ids(user_in.role_ids)
            db_user.roles = roles

        if user_in.sector_ids:
            # --- MEJORA: Usar el SectorRepository para mantener la arquitectura limpia ---
            sectors = self.sector_repo.get_by_ids(user_in.sector_ids)
            db_user.assigned_sectors = sectors

        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
