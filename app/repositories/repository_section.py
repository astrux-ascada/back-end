# Funciones de Repositorio para el modelo Section

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.models.plant import Section
from app.schemas.section import SectionCreate


async def get(db: AsyncSession, id: int):
    """Obtiene una sección por su ID."""
    result = await db.execute(select(Section).filter(Section.id == id))
    return result.scalars().first()


async def get_by_name(db: AsyncSession, name: str):
    """Obtiene una sección por su nombre."""
    result = await db.execute(select(Section).filter(Section.name == name))
    return result.scalars().first()


async def get_multi(db: AsyncSession, skip: int = 0, limit: int = 100):
    """Obtiene una lista de secciones."""
    result = await db.execute(select(Section).offset(skip).limit(limit))
    return result.scalars().all()


async def create(db: AsyncSession, obj_in: SectionCreate):
    """Crea una nueva sección."""
    db_obj = Section(name=obj_in.name, description=obj_in.description)
    db.add(db_obj)
    await db.commit()
    await db.refresh(db_obj)
    return db_obj
