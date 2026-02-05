"""
Módulo de agregación para los routers de la API v1.
"""

from fastapi import APIRouter, Depends

# --- Dependencia de Feature Flags ---
from app.dependencies.subscription import require_feature

# --- Routers de Módulos de Astruxa ---
from app.identity import api as identity_api
from app.identity import api_roles as identity_roles_api
from app.identity import api_saas as saas_api
from app.assets import api as assets_api
from app.telemetry import api as telemetry_api
from app.procurement import api as procurement_api
from app.maintenance import api as maintenance_api
from app.core_engine import api as core_engine_api
from app.sectors import api as sectors_api
from app.auditing import api as auditing_api
from app.configuration import api as configuration_api
from app.alarming import api as alarming_api
from app.notifications import api as notifications_api
from app.media import api as media_api

# --- Definición de los nuevos routers por capa ---

# Router para operaciones de planta (Técnicos, Supervisores)
ops_router = APIRouter(prefix="/ops")
ops_router.include_router(assets_api.router, dependencies=[Depends(require_feature("module_assets"))])
ops_router.include_router(maintenance_api.router, dependencies=[Depends(require_feature("module_maintenance"))])
ops_router.include_router(procurement_api.router, dependencies=[Depends(require_feature("module_procurement"))])
ops_router.include_router(telemetry_api.router, dependencies=[Depends(require_feature("module_telemetry"))])
ops_router.include_router(alarming_api.router, dependencies=[Depends(require_feature("module_alarming"))])
ops_router.include_router(media_api.router) # Media Manager es una operación básica, no se monetiza por separado

# Router para la gestión del cliente (Tenant Admins)
back_office_router = APIRouter(prefix="/back-office")
back_office_router.include_router(identity_roles_api.router) # La gestión de usuarios/roles es básica
back_office_router.include_router(sectors_api.router) # La gestión de sectores es básica
back_office_router.include_router(auditing_api.router, dependencies=[Depends(require_feature("module_auditing"))]) # La auditoría es una feature premium

# Router para la gestión del sistema (Platform Admins, Partners)
sys_mgt_router = APIRouter(prefix="/sys-mgt")
sys_mgt_router.include_router(configuration_api.router)
sys_mgt_router.include_router(saas_api.router)
sys_mgt_router.include_router(core_engine_api.router) # La configuración de DataSources es parte de la gestión

# --- Router Principal de la API v1 ---
api_router = APIRouter(prefix="/api/v1")

# Endpoints de autenticación se mantienen en la raíz de /api/v1
api_router.include_router(identity_api.router) 

# Anidar los nuevos routers por capa
api_router.include_router(ops_router)
api_router.include_router(back_office_router)
api_router.include_router(sys_mgt_router)

# Routers transversales (ej: notificaciones)
api_router.include_router(notifications_api.router)
