"""
Módulo de agregación para los routers de la API v1.
"""

from fastapi import APIRouter, Depends

# --- Dependencias de Suscripción y Permisos ---
from app.dependencies.subscription import require_feature, require_active_subscription
from app.dependencies.permissions import require_permission

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

# --- Router Principal de la API v1 ---
# Todos los endpoints bajo este router requerirán una suscripción activa,
# excepto los que estén en la lista blanca de la dependencia.
api_router = APIRouter(dependencies=[Depends(require_active_subscription)])

# --- Endpoints de Autenticación (Públicos o con su propia lógica) ---
# No se les aplica el `require_active_subscription` globalmente.
auth_router = APIRouter()
auth_router.include_router(identity_api.router)
auth_router.include_router(saas_api.router) # El registro público y la gestión de planes no deben requerir suscripción activa.

# --- Routers Operativos (Protegidos por Suscripción Activa) ---
ops_router = APIRouter(prefix="/ops")
ops_router.include_router(assets_api.router, dependencies=[Depends(require_feature("module_assets"))])
ops_router.include_router(maintenance_api.router, dependencies=[Depends(require_feature("module_maintenance"))])
ops_router.include_router(procurement_api.router, dependencies=[Depends(require_feature("module_procurement"))])
ops_router.include_router(telemetry_api.router, dependencies=[Depends(require_feature("module_telemetry"))])
ops_router.include_router(alarming_api.router, dependencies=[Depends(require_feature("module_alarming"))])
ops_router.include_router(media_api.router)

back_office_router = APIRouter(prefix="/back-office")
back_office_router.include_router(identity_roles_api.router)
back_office_router.include_router(sectors_api.router)
back_office_router.include_router(auditing_api.router, dependencies=[Depends(require_feature("module_auditing"))])

sys_mgt_router = APIRouter(prefix="/sys-mgt")
sys_mgt_router.include_router(configuration_api.router)
sys_mgt_router.include_router(core_engine_api.router)

# --- Montaje Final ---
api_router.include_router(auth_router) # Rutas de autenticación y SaaS
api_router.include_router(ops_router) # Rutas operativas
api_router.include_router(back_office_router) # Rutas de gestión de tenant
api_router.include_router(sys_mgt_router) # Rutas de gestión de sistema
api_router.include_router(notifications_api.router) # Notificaciones es transversal
