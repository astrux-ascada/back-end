# Endpoints de la API para el modelo Section
import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import repository_section
from app.schemas.section import Section, SectionCreate
from app.core.database import get_db

router = APIRouter()


@router.post("/", response_model=Section)
async def create_section(
    *, 
    db: AsyncSession = Depends(get_db), 
    section_in: SectionCreate
):
    """
    Crea una nueva sección.
    """
    # Comprueba si ya existe una sección con el mismo nombre
    existing_section = await repository_section.get_by_name(db, name=section_in.name)
    if existing_section:
        raise HTTPException(
            status_code=400, 
            detail="Ya existe una sección con este nombre."
        )
    
    # Crea la nueva sección
    section = await repository_section.create(db=db, obj_in=section_in)
    return section


@router.get("/", response_model=List[Section])
async def read_sections(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    Obtiene una lista de secciones.
    """
    sections = await repository_section.get_multi(db, skip=skip, limit=limit)
    return sections


@router.get("/{section_id}", response_model=Section)
async def read_section_by_id(
    section_id: uuid.UUID,
    db: AsyncSession = Depends(get_db),
):
    """
    Obtiene una sección por su ID.
    """
    section = await repository_section.get(db, id=section_id)
    if not section:
        raise HTTPException(status_code=404, detail="Sección no encontrada.")
    return section
