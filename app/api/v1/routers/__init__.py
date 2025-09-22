"""
Módulo de agregación para los routers de la API v1.
"""

from fastapi import APIRouter

from app.assets import api as assets_api
from app.core_engine import api as core_engine_api
# --- Routers de Módulos de Astruxa ---
from app.identity import api as identity_api
from app.maintenance import api as maintenance_api
from app.procurement import api as procurement_api
from app.telemetry import api as telemetry_api

# --- Routers antiguos (se irán eliminando) ---


api_router = APIRouter(prefix="/api/v1")

# --- REGISTRO DE ROUTERS NUEVOS ---
api_router.include_router(identity_api.router, prefix="/auth")
api_router.include_router(assets_api.router)  # El prefijo "/assets" ya está en el router
api_router.include_router(telemetry_api.router)  # El prefijo "/telemetry" ya está en el router
api_router.include_router(procurement_api.router)  # El prefijo "/procurement" ya está en el router
api_router.include_router(maintenance_api.router)  # El prefijo "/maintenance" ya está en el router
api_router.include_router(core_engine_api.router)  # El prefijo "/core-engine" ya está en el router
