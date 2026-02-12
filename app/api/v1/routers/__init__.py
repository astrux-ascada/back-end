"""
Módulo de agregación para los routers de la API v1.
"""

from fastapi import APIRouter, Depends

# --- Dependencias ---
from app.dependencies.subscription import require_feature, require_active_subscription
from app.dependencies.permissions import require_permission

# --- Routers de Módulos ---
from app.identity import api as identity_api, api_roles, api_saas, sys_admin_api
from app.identity import api_marketing # <-- Nuevo
from app.assets import api as assets_api
# ... (resto de imports)

# --- Router Principal ---
api_router = APIRouter()

# --- Endpoints de Autenticación y SaaS (Públicos y de Cliente) ---
saas_router = APIRouter(prefix="/saas")
saas_router.include_router(api_saas.router)
saas_router.include_router(api_marketing.client_router) # <-- Montamos el router de cliente aquí

auth_router = APIRouter()
auth_router.include_router(identity_api.router)
auth_router.include_router(saas_router) # Anidamos SaaS bajo la autenticación general

# --- Routers Operativos (Protegidos por Suscripción) ---
ops_router = APIRouter(prefix="/ops", dependencies=[Depends(require_active_subscription)])
# ... (endpoints operativos)

# --- Routers de Back-Office (Protegidos por Suscripción) ---
back_office_router = APIRouter(prefix="/back-office", dependencies=[Depends(require_active_subscription)])
# ... (endpoints de back-office)

# --- Routers de Gestión de Sistema (Super Admin) ---
sys_mgt_router = APIRouter(prefix="/sys-mgt")
sys_mgt_router.include_router(sys_admin_api.router, prefix="/identity") # CRUD de usuarios globales
sys_mgt_router.include_router(api_marketing.admin_router) # <-- CRUD de Campañas/Cupones
# ... (otros endpoints de sistema)


# --- Montaje Final ---
api_router.include_router(auth_router)
api_router.include_router(ops_router)
api_router.include_router(back_office_router)
api_router.include_router(sys_mgt_router)
# ... (resto de montaje)
