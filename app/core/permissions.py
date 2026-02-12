# /app/core/permissions.py
"""
Definición centralizada de todos los permisos disponibles en la aplicación.
"""

# --- Permisos de Módulos SaaS ---
PLAN_READ = "plan:read"
PLAN_CREATE = "plan:create"
PLAN_UPDATE = "plan:update"

TENANT_READ = "tenant:read"
TENANT_READ_ALL = "tenant:read_all"
TENANT_CREATE = "tenant:create"
TENANT_UPDATE = "tenant:update"
TENANT_ASSIGN_MANAGER = "tenant:assign_manager"
TENANT_DELETE_REQUEST = "tenant:delete_request"
TENANT_DELETE_APPROVE = "tenant:delete_approve"
TENANT_DELETE_FORCE = "tenant:delete_force"

SUBSCRIPTION_READ = "subscription:read"
SUBSCRIPTION_UPDATE = "subscription:update"

# --- Permisos de Marketing y Ventas ---
CAMPAIGN_READ = "campaign:read"
CAMPAIGN_CREATE = "campaign:create"
CAMPAIGN_UPDATE = "campaign:update"
CAMPAIGN_DELETE = "campaign:delete"

COUPON_READ = "coupon:read"
COUPON_CREATE = "coupon:create"
COUPON_UPDATE = "coupon:update"
COUPON_DELETE = "coupon:delete"
# Permiso especial para que un cliente aplique un cupón
COUPON_APPLY = "coupon:apply"

REFERRAL_READ = "referral:read"

# --- Permisos de Módulos Operativos ---
ASSET_READ = "asset:read"
ASSET_CREATE = "asset:create"
ASSET_UPDATE = "asset:update"
ASSET_UPDATE_STATUS = "asset:update_status"
ASSET_DELETE = "asset:delete"

WORK_ORDER_READ = "work_order:read"
WORK_ORDER_CREATE = "work_order:create"
WORK_ORDER_UPDATE = "work_order:update"
WORK_ORDER_CANCEL = "work_order:cancel"
WORK_ORDER_ASSIGN_PROVIDER = "work_order:assign_provider"
WORK_ORDER_EVALUATE = "work_order:evaluate"

# ... (resto de permisos operativos)

# --- Permisos de Usuario y Roles (Identity) ---
USER_READ = "user:read"
USER_CREATE = "user:create"
USER_UPDATE = "user:update"
USER_DELETE = "user:delete"

USER_READ_ALL = "user:read_all"
USER_CREATE_ANY = "user:create_any"
USER_UPDATE_ANY = "user:update_any"
USER_DELETE_ANY = "user:delete_any"

USER_CREATE_ADMIN = "user:create_admin"

ROLE_READ = "role:read"
ROLE_CREATE = "role:create"
ROLE_UPDATE = "role:update"
ROLE_DELETE = "role:delete"

PERMISSION_READ = "permission:read"
SESSION_DELETE = "session:delete"

# --- Conjuntos de Permisos por Rol ---

DEFAULT_TENANT_ADMIN_PERMISSIONS = [
    TENANT_READ, TENANT_UPDATE,
    ASSET_READ, ASSET_CREATE, ASSET_UPDATE, ASSET_DELETE,
    # ... (resto de permisos de tenant)
    USER_READ, USER_CREATE, USER_UPDATE, USER_DELETE,
    ROLE_READ, ROLE_CREATE, ROLE_UPDATE, ROLE_DELETE,
    COUPON_APPLY, # Permitir que el admin del tenant aplique un cupón
]

DEFAULT_PLATFORM_ADMIN_PERMISSIONS = [
    PLAN_READ, PLAN_CREATE, PLAN_UPDATE,
    TENANT_READ, TENANT_CREATE, TENANT_UPDATE, TENANT_DELETE_REQUEST,
    SUBSCRIPTION_READ, SUBSCRIPTION_UPDATE,
    USER_READ_ALL, USER_CREATE_ANY, USER_UPDATE_ANY, USER_DELETE_ANY,
    # Permisos de Marketing
    CAMPAIGN_READ, CAMPAIGN_CREATE, CAMPAIGN_UPDATE, CAMPAIGN_DELETE,
    COUPON_READ, COUPON_CREATE, COUPON_UPDATE, COUPON_DELETE,
    REFERRAL_READ,
]
