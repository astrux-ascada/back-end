# /app/identity/repository.py
"""
Capa de Repositorio para la entidad User.

Encapsula toda la lógica de acceso a datos (CRUD) para el modelo User,
actuando como una abstracción entre la lógica de negocio y la base de datos.
"""

import uuid
from sqlalchemy.orm import Session

from app.core.security import hash_password
from app.identity.models import User
from app.identity.schemas import UserCreate


class UserRepository:
    """Realiza operaciones CRUD en la base de datos para el modelo User."""

    def __init__(self, db: Session):
        self.db = db

    def get_by_id(self, user_id: uuid.UUID) -> User | None:
        """Busca un usuario por su ID."""
        return self.db.query(User).filter(User.id == user_id).first()

    def get_by_email(self, email: str) -> User | None:
        """Busca un usuario por su dirección de email."""
        return self.db.query(User).filter(User.email == email).first()

    def create(self, user_in: UserCreate) -> User:
        """
        Crea un nuevo registro de usuario en la base de datos a partir de un esquema Pydantic.
        Hashea la contraseña antes de guardarla.
        """
        user_data = user_in.model_dump(exclude={"password"})
        hashed_password = hash_password(user_in.password)
        user_data["hashed_password"] = hashed_password

        db_user = User(**user_data)

        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)

        return db_user
