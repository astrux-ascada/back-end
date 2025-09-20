# Endpoints para la autenticación de usuarios

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.repositories import repository_user
from app.core.security import create_access_token, verify_password
from app.schemas.token import Token
from app.core.database import get_db

router = APIRouter()


@router.post("/login/token", response_model=Token)
async def login_for_access_token(
    db: AsyncSession = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
):
    """
    Autentica a un usuario y devuelve un token de acceso JWT.
    """
    # 1. Busca al usuario por su email (que en el form de OAuth2 se llama `username`)
    user = await repository_user.get_by_email(db, email=form_data.username)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 2. Verifica que la contraseña sea correcta
    if not verify_password(form_data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # 3. Crea y devuelve el token de acceso
    access_token = create_access_token(subject=user.id)
    return {"access_token": access_token, "token_type": "bearer"}
