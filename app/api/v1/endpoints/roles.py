# Endpoints de la API para el modelo Role
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import repository_role
from app.schemas.role import Role, RoleCreate
from app.core.database import get_db

router = APIRouter()


@router.post("/", response_model=Role)
async def create_role(
    *, 
    db: AsyncSession = Depends(get_db), 
    role_in: RoleCreate
):
    """
    Crea un nuevo rol.
    """
    existing_role = await repository_role.get_by_name(db, name=role_in.name)
    if existing_role:
        raise HTTPException(
            status_code=400, 
            detail="Ya existe un rol con este nombre."
        )
    
    role = await repository_role.create(db=db, obj_in=role_in)
    return role


@router.get("/", response_model=List[Role])
async def read_roles(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    Obtiene una lista de roles.
    """
    roles = await repository_role.get_multi(db, skip=skip, limit=limit)
    return roles
