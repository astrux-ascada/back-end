# /app/db/base.py
"""
Importa todos los modelos del sistema para que Alembic pueda detectarlos.
"""
from app.db.base_class import Base

# 1. Identity & SaaS
from app.identity.models.user import User
from app.identity.models.role import Role
from app.identity.models.permission import Permission
from app.identity.models.saas.partner import Partner
from app.identity.models.saas.plan import Plan
from app.identity.models.saas.tenant import Tenant
from app.identity.models.saas.subscription import Subscription

# 2. Maintenance
from app.maintenance.models.work_order import WorkOrder
from app.maintenance.models.maintenance_task import MaintenanceTask
from app.maintenance.models.maintenance_plan import MaintenancePlan
from app.maintenance.models.maintenance_plan_task import MaintenancePlanTask
from app.maintenance.models.work_order_user_assignment import WorkOrderUserAssignment
from app.maintenance.models.work_order_provider_assignment import WorkOrderProviderAssignment

# 3. Procurement
from app.procurement.models.provider import Provider
from app.procurement.models.spare_part import SparePart

# 4. Alarming
from app.alarming.models import AlarmRule, Alarm

# 5. Notifications
from app.notifications.models.notification import Notification
from app.notifications.models.notification_config import NotificationTemplate, NotificationChannel, NotificationRule

# 6. Sectors
from app.sectors.models.sector import Sector

# 7. Configuration
from app.configuration.models.configuration_parameter import ConfigurationParameter
from app.configuration.models.enum_type import EnumType
from app.configuration.models.enum_value import EnumValue

# 8. Assets
from app.assets.models.asset import Asset

# 9. Auditing
from app.auditing.models.audit_log import AuditLog
from app.auditing.models.approval_request import ApprovalRequest

# 10. Telemetry
from app.telemetry.models.sensor_reading import SensorReading

# 11. Core Engine
from app.core_engine.models.data_source import DataSource
from app.core_engine.models.machine_state_history import MachineStateHistory

# 12. Media
from app.media.models import MediaItem
