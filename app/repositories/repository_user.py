# Funciones de Repositorio para el modelo User
import uuid
from typing import List, Optional

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.models.identity import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash


async def get(db: AsyncSession, id: uuid.UUID) -> Optional[User]:
    """Obtiene un usuario por su ID."""
    result = await db.execute(select(User).filter(User.id == id))
    return result.scalars().first()


async def get_by_email(db: AsyncSession, email: str) -> Optional[User]:
    """Obtiene un usuario por su email."""
    result = await db.execute(select(User).filter(User.email == email))
    return result.scalars().first()


async def get_multi(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[User]:
    """Obtiene una lista de usuarios."""
    result = await db.execute(select(User).offset(skip).limit(limit))
    return result.scalars().all()


async def create(db: AsyncSession, obj_in: UserCreate) -> User:
    """Crea un nuevo usuario."""
    hashed_password = get_password_hash(obj_in.password)
    db_obj = User(
        email=obj_in.email,
        name=obj_in.name,
        password_hash=hashed_password,
        role_id=obj_in.role_id
    )
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj
