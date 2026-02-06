# /app/core/permissions.py
"""
Definición centralizada de todos los permisos disponibles en la aplicación.
"""

# --- Permisos de Módulos SaaS ---
PLAN_READ = "plan:read"
PLAN_CREATE = "plan:create"
PLAN_UPDATE = "plan:update"

TENANT_READ = "tenant:read"
TENANT_CREATE = "tenant:create"
TENANT_UPDATE = "tenant:update"

SUBSCRIPTION_READ = "subscription:read"
SUBSCRIPTION_UPDATE = "subscription:update"

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

PROVIDER_READ = "provider:read"
PROVIDER_CREATE = "provider:create"
PROVIDER_UPDATE = "provider:update"
PROVIDER_DELETE = "provider:delete"

SPARE_PART_READ = "spare_part:read"
SPARE_PART_CREATE = "spare_part:create"
SPARE_PART_UPDATE = "spare_part:update"
SPARE_PART_DELETE = "spare_part:delete"

# --- Permisos del Flujo de Compras Inteligente ---
RFQ_CREATE = "rfq:create"
RFQ_READ = "rfq:read"
QUOTE_SUBMIT = "quote:submit" # Para proveedores
QUOTE_EVALUATE = "quote:evaluate" # Para gestores
PO_CREATE = "po:create"
PO_READ = "po:read"
PO_RECEIVE = "po:receive" # Añadido

ALARM_RULE_READ = "alarm_rule:read"
ALARM_RULE_CREATE = "alarm_rule:create"
ALARM_RULE_UPDATE = "alarm_rule:update"
ALARM_RULE_DELETE = "alarm_rule:delete"

ALARM_READ = "alarm:read"
ALARM_ACKNOWLEDGE = "alarm:acknowledge"

SECTOR_READ = "sector:read"
SECTOR_CREATE = "sector:create"
SECTOR_UPDATE = "sector:update"
SECTOR_DELETE = "sector:delete"

CONFIG_PARAM_READ = "config_param:read"
CONFIG_PARAM_CREATE = "config_param:create"
CONFIG_PARAM_UPDATE = "config_param:update"
CONFIG_PARAM_DELETE = "config_param:delete"

DATA_SOURCE_READ = "data_source:read"
DATA_SOURCE_CREATE = "data_source:create"
DATA_SOURCE_UPDATE = "data_source:update"
DATA_SOURCE_DELETE = "data_source:delete"

# --- Permisos de Auditoría y Aprobaciones ---
AUDIT_LOG_READ = "audit_log:read"
APPROVAL_READ = "approval:read"
APPROVAL_DECIDE = "approval:decide"

# --- Permisos de Usuario y Roles (Identity) ---
USER_READ = "user:read"
USER_CREATE = "user:create"
USER_UPDATE = "user:update"
USER_DELETE = "user:delete"

ROLE_READ = "role:read"
ROLE_CREATE = "role:create"
ROLE_UPDATE = "role:update"
ROLE_DELETE = "role:delete"

PERMISSION_READ = "permission:read"

# --- Permisos de Sesión ---
SESSION_DELETE = "session:delete"

# --- Conjuntos de Permisos por Rol ---

DEFAULT_TENANT_ADMIN_PERMISSIONS = [
    ASSET_READ, ASSET_CREATE, ASSET_UPDATE, ASSET_DELETE,
    WORK_ORDER_READ, WORK_ORDER_CREATE, WORK_ORDER_UPDATE, WORK_ORDER_CANCEL, WORK_ORDER_ASSIGN_PROVIDER,
    PROVIDER_READ, PROVIDER_CREATE, PROVIDER_UPDATE, PROVIDER_DELETE,
    SPARE_PART_READ, SPARE_PART_CREATE, SPARE_PART_UPDATE, SPARE_PART_DELETE,
    ALARM_RULE_READ, ALARM_RULE_CREATE, ALARM_RULE_UPDATE, ALARM_RULE_DELETE,
    ALARM_READ, ALARM_ACKNOWLEDGE,
    SECTOR_READ, SECTOR_CREATE, SECTOR_UPDATE, SECTOR_DELETE,
    AUDIT_LOG_READ, APPROVAL_READ, APPROVAL_DECIDE,
    USER_READ, USER_CREATE, USER_UPDATE, USER_DELETE,
    ROLE_READ, ROLE_CREATE, ROLE_UPDATE, ROLE_DELETE,
]
