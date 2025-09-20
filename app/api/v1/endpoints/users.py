# Endpoints de la API para el modelo User
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import repository_user, repository_role
from app.schemas.user import User, UserCreate
from app.core.database import get_db

router = APIRouter()


@router.post("/", response_model=User)
async def create_user(
    *, 
    db: AsyncSession = Depends(get_db), 
    user_in: UserCreate
):
    """
    Crea un nuevo usuario.
    """
    # 1. Comprueba si ya existe un usuario con el mismo email
    existing_user = await repository_user.get_by_email(db, email=user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=400, 
            detail="Ya existe un usuario con este email."
        )

    # 2. Comprueba si el rol asignado existe
    existing_role = await repository_role.get(db, id=user_in.role_id)
    if not existing_role:
        raise HTTPException(
            status_code=404,
            detail=f"El rol con id {user_in.role_id} no fue encontrado."
        )

    # 3. Crea el nuevo usuario (el repositorio se encarga del hashing)
    user = await repository_user.create(db=db, obj_in=user_in)
    return user


@router.get("/", response_model=List[User])
async def read_users(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
):
    """
    Obtiene una lista de usuarios.
    """
    users = await repository_user.get_multi(db, skip=skip, limit=limit)
    return users
