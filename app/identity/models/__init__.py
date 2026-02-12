# /app/identity/models/__init__.py
"""
Expone los modelos del módulo de identidad y define sus interrelaciones
para evitar dependencias circulares.
"""

from sqlalchemy.orm import relationship

# --- 1. Importar todas las clases de modelo necesarias ---

# Modelos de este módulo
from .user import User
from .role import Role
from .permission import Permission
from .role_permission_association import RolePermissionAssociation
from .user_role_association import UserRoleAssociation
from .user_sector_association import UserSectorAssociation

# Modelos SaaS (Multi-Tenancy)
from .saas.partner import Partner
from .saas.plan import Plan
from .saas.tenant import Tenant
from .saas.subscription import Subscription

# Modelos de Marketing (Cupones, Campañas, Referidos)
from .saas.marketing import MarketingCampaign, Coupon, Referral

# Modelos de otros módulos con los que nos relacionamos
from app.sectors.models.sector import Sector


# --- 2. Definir las relaciones inversas (back-populates) ---
# Ahora que todas las clases están en el mismo ámbito, podemos crear los "puentes".

# Relación User <-> Sector
User.assigned_sectors = relationship("Sector", secondary="user_sectors", back_populates="users")
Sector.users = relationship("User", secondary="user_sectors", back_populates="assigned_sectors")

# Relación Tenant <-> Referral
# Un tenant puede referir a muchos (referrer) y ser referido por uno (referee)
Tenant.referrals_made = relationship("Referral", foreign_keys=[Referral.referrer_tenant_id], back_populates="referrer")
Tenant.referral_received = relationship("Referral", foreign_keys=[Referral.referred_tenant_id], uselist=False, back_populates="referee")

Referral.referrer = relationship("Tenant", foreign_keys=[Referral.referrer_tenant_id], back_populates="referrals_made")
Referral.referee = relationship("Tenant", foreign_keys=[Referral.referred_tenant_id], back_populates="referral_received")

# Relación Subscription <-> Coupon
# Añadimos la relación a la suscripción para saber qué cupón se aplicó
Subscription.applied_coupon = relationship("Coupon")
