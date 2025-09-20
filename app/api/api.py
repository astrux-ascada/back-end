# Enrutador principal de la API

from fastapi import APIRouter

from app.api.v1.endpoints import login, sections, roles, users

api_router = APIRouter()

# Incluye los endpoints de la v1
api_router.include_router(login.router, tags=["Authentication"])
api_router.include_router(sections.router, prefix="/sections", tags=["Sections"])
api_router.include_router(roles.router, prefix="/roles", tags=["Roles"])
api_router.include_router(users.router, prefix="/users", tags=["Users"])
