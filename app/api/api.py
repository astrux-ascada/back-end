# Enrutador principal de la API

from fastapi import APIRouter

from app.api.v1.endpoints import sections

api_router = APIRouter()

# Incluye los endpoints de la v1
api_router.include_router(sections.router, prefix="/sections", tags=["Sections"])
