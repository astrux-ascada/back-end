# Funciones de Repositorio para el modelo Role
import uuid
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.models.identity import Role
from app.schemas.role import RoleCreate


async def get(db: AsyncSession, id: uuid.UUID) -> Role | None:
    """Obtiene un rol por su ID."""
    result = await db.execute(select(Role).filter(Role.id == id))
    return result.scalars().first()


async def get_by_name(db: AsyncSession, name: str) -> Role | None:
    """Obtiene un rol por su nombre."""
    result = await db.execute(select(Role).filter(Role.name == name))
    return result.scalars().first()


async def get_multi(db: AsyncSession, skip: int = 0, limit: int = 100) -> list[Role]:
    """Obtiene una lista de roles."""
    result = await db.execute(select(Role).offset(skip).limit(limit))
    return result.scalars().all()


async def create(db: AsyncSession, obj_in: RoleCreate) -> Role:
    """Crea un nuevo rol."""
    db_obj = Role(name=obj_in.name, description=obj_in.description)
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj
