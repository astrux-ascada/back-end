"""add_saas_models_final

Revision ID: 62bdc06ef135
Revises: 0014
Create Date: 2026-02-02 18:44:04.382332

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '62bdc06ef135'
down_revision: Union[str, None] = '0014'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### Comandos seguros para la arquitectura SaaS ###
    
    # 1. Crear tabla 'partners'
    op.create_table('partners',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('code', sa.String(length=50), nullable=False, comment='Código único del partner (ej: ASTRUXA_MX)'),
        sa.Column('name', sa.String(length=100), nullable=False, comment='Nombre legal del partner'),
        sa.Column('region', sa.String(length=50), nullable=False, comment='Región operativa (ej: LATAM, EMEA)'),
        sa.Column('currency', sa.String(length=3), nullable=False, comment='Moneda base para facturación (ISO 4217)'),
        sa.Column('tax_id', sa.String(length=50), nullable=True, comment='Identificación fiscal del partner'),
        sa.Column('commission_rate', sa.Float(), nullable=False, comment='Porcentaje de comisión sobre ventas'),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('config', sa.JSON(), nullable=False, comment='Configuración específica del partner (logos, soporte, etc)'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_partners_code'), 'partners', ['code'], unique=True)

    # 2. Crear tabla 'plans'
    op.create_table('plans',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('code', sa.String(length=50), nullable=False, comment='Código inmutable del plan (ej: ENTERPRISE_2024)'),
        sa.Column('name', sa.String(length=100), nullable=False, comment='Nombre comercial del plan'),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('price_monthly', sa.Float(), nullable=False),
        sa.Column('price_yearly', sa.Float(), nullable=False),
        sa.Column('currency', sa.String(length=3), nullable=False),
        sa.Column('limits', sa.JSON(), nullable=False, comment='Cuotas técnicas: {max_users: 10, max_assets: 100}'),
        sa.Column('features', sa.JSON(), nullable=False, comment="Flags de módulos: {module_procurement: true, isolation: 'SHARED'}"),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_public', sa.Boolean(), nullable=False, comment='Si es visible en la página de precios pública'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_plans_code'), 'plans', ['code'], unique=True)

    # 3. Crear tabla 'tenants'
    op.create_table('tenants',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('partner_id', sa.UUID(), nullable=True, comment='Partner que gestiona este tenant. NULL = Directo Global'),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('slug', sa.String(length=50), nullable=False, comment='Identificador URL-friendly (ej: coca-cola-mx)'),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('db_connection_string', sa.String(), nullable=True, comment='Si NULL, usa DB compartida. Si tiene valor, usa DB dedicada.'),
        sa.Column('logo_url', sa.String(), nullable=True),
        sa.Column('timezone', sa.String(length=50), nullable=False),
        sa.Column('locale', sa.String(length=10), nullable=False),
        sa.Column('config', sa.JSON(), nullable=False, comment='Configuración específica del tenant (colores, preferencias)'),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['partner_id'], ['partners.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tenants_name'), 'tenants', ['name'], unique=False)
    op.create_index(op.f('ix_tenants_slug'), 'tenants', ['slug'], unique=True)

    # 4. Crear tabla 'subscriptions'
    op.create_table('subscriptions',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('tenant_id', sa.UUID(), nullable=False),
        sa.Column('plan_id', sa.UUID(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('current_period_start', sa.TIMESTAMP(timezone=True), nullable=False),
        sa.Column('current_period_end', sa.TIMESTAMP(timezone=True), nullable=False, comment='Fecha de vencimiento/renovación'),
        sa.Column('trial_end', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('canceled_at', sa.TIMESTAMP(timezone=True), nullable=True),
        sa.Column('payment_method_id', sa.String(), nullable=True, comment='ID del método de pago en Stripe/PayPal'),
        sa.Column('billing_email', sa.String(), nullable=True),
        sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['plan_id'], ['plans.id'], ),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('tenant_id')
    )

    # 5. Añadir columnas a la tabla 'users'
    op.add_column('users', sa.Column('tenant_id', sa.UUID(), nullable=True, comment='Organización a la que pertenece. NULL = Super Admin Global'))
    op.add_column('users', sa.Column('failed_login_attempts', sa.Integer(), nullable=False, server_default='0', comment='Contador de intentos fallidos consecutivos'))
    op.add_column('users', sa.Column('locked_until', sa.TIMESTAMP(timezone=True), nullable=True, comment='Fecha hasta la cual el usuario está bloqueado temporalmente'))
    op.add_column('users', sa.Column('last_login_at', sa.TIMESTAMP(timezone=True), nullable=True))
    op.add_column('users', sa.Column('last_login_ip', sa.String(length=45), nullable=True))
    op.add_column('users', sa.Column('terms_accepted_at', sa.TIMESTAMP(timezone=True), nullable=True, comment='Fecha de aceptación de los términos'))
    op.add_column('users', sa.Column('terms_version', sa.String(length=20), nullable=True, comment='Versión de los términos aceptada (ej: v1.2)'))
    op.create_foreign_key('fk_users_tenant_id', 'users', 'tenants', ['tenant_id'], ['id'])


def downgrade() -> None:
    # ### Comandos para revertir la arquitectura SaaS ###
    op.drop_constraint('fk_users_tenant_id', 'users', type_='foreignkey')
    op.drop_column('users', 'terms_version')
    op.drop_column('users', 'terms_accepted_at')
    op.drop_column('users', 'last_login_ip')
    op.drop_column('users', 'last_login_at')
    op.drop_column('users', 'locked_until')
    op.drop_column('users', 'failed_login_attempts')
    op.drop_column('users', 'tenant_id')
    
    op.drop_table('subscriptions')
    op.drop_index(op.f('ix_tenants_slug'), table_name='tenants')
    op.drop_index(op.f('ix_tenants_name'), table_name='tenants')
    op.drop_table('tenants')
    op.drop_index(op.f('ix_plans_code'), table_name='plans')
    op.drop_table('plans')
    op.drop_index(op.f('ix_partners_code'), table_name='partners')
    op.drop_table('partners')
