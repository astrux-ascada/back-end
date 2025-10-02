"""
Módulo de agregación para los routers de la API v1.

Este archivo importa los routers de los módulos de dominio de Astruxa
y los une en un único APIRouter para ser incluido en la aplicación principal.
"""

from fastapi import APIRouter

# --- Routers de Módulos de Astruxa ---
from app.identity import api as identity_api
from app.assets import api as assets_api
from app.telemetry import api as telemetry_api
from app.procurement import api as procurement_api
from app.maintenance import api as maintenance_api
from app.core_engine import api as core_engine_api
from app.sectors import api as sectors_api
from app.auditing import api as auditing_api
from app.configuration import api as configuration_api
from app.alarming import api as alarming_api # Añadido el nuevo router


api_router = APIRouter(prefix="/api/v1")

# --- REGISTRO DE ROUTERS DE MÓDULOS ---
api_router.include_router(identity_api.router)
api_router.include_router(assets_api.router)
api_router.include_router(telemetry_api.router)
api_router.include_router(procurement_api.router)
api_router.include_router(maintenance_api.router)
api_router.include_router(core_engine_api.router)
api_router.include_router(sectors_api.router)
api_router.include_router(auditing_api.router)
api_router.include_router(configuration_api.router)
api_router.include_router(alarming_api.router) # El prefijo "/alarming" ya está en el router
