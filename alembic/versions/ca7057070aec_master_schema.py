"""master_schema

Revision ID: ca7057070aec
Revises: 
Create Date: 2026-02-05 11:15:00.123456

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = 'ca7057070aec'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### FASE 1: Tablas sin dependencias ###
    op.create_table('asset_types',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('category', sa.String(length=50), nullable=True),
        sa.Column('properties_schema', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_asset_types_category'), 'asset_types', ['category'], unique=False)
    op.create_index(op.f('ix_asset_types_name'), 'asset_types', ['name'], unique=True)

    op.create_table('partners',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('code', sa.String(length=20), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('commission_rate', sa.Float(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_partners_code'), 'partners', ['code'], unique=True)

    op.create_table('permissions',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_permissions_name'), 'permissions', ['name'], unique=True)

    op.create_table('plans',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('code', sa.String(length=50), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('price_monthly', sa.Float(), nullable=False),
        sa.Column('price_yearly', sa.Float(), nullable=False),
        sa.Column('currency', sa.String(length=3), nullable=False),
        sa.Column('limits', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('features', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_plans_code'), 'plans', ['code'], unique=True)

    # ### FASE 2: Tablas que dependen de la FASE 1 ###
    op.create_table('tenants',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('slug', sa.String(length=100), nullable=False),
        sa.Column('partner_id', sa.UUID(), nullable=True),
        sa.ForeignKeyConstraint(['partner_id'], ['partners.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tenants_name'), 'tenants', ['name'], unique=False)
    op.create_index(op.f('ix_tenants_slug'), 'tenants', ['slug'], unique=True)

    # ### FASE 3: Tablas que dependen de TENANTS y otras tablas base ###
    op.create_table('data_sources',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('tenant_id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('protocol', sa.String(), nullable=False),
        sa.Column('connection_params', postgresql.JSONB(astext_type=sa.Text()), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_data_sources_is_active'), 'data_sources', ['is_active'], unique=False)
    op.create_index(op.f('ix_data_sources_name'), 'data_sources', ['name'], unique=False)
    op.create_index(op.f('ix_data_sources_protocol'), 'data_sources', ['protocol'], unique=False)
    op.create_index(op.f('ix_data_sources_tenant_id'), 'data_sources', ['tenant_id'], unique=False)

    op.create_table('providers',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('contact_info', sa.String(length=255), nullable=True),
        sa.Column('specialty', sa.String(length=100), nullable=True),
        sa.Column('performance_score', sa.Float(), nullable=True),
        sa.Column('tenant_id', sa.UUID(), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_providers_name'), 'providers', ['name'], unique=False)
    op.create_index(op.f('ix_providers_tenant_id'), 'providers', ['tenant_id'], unique=False)

    op.create_table('roles',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('tenant_id', sa.UUID(), nullable=True),
        sa.Column('name', sa.String(length=50), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_roles_name'), 'roles', ['name'], unique=False)
    op.create_index(op.f('ix_roles_tenant_id'), 'roles', ['tenant_id'], unique=False)

    op.create_table('sectors',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('tenant_id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.String(length=255), nullable=True),
        sa.Column('parent_id', sa.UUID(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['parent_id'], ['sectors.id'], ),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sectors_name'), 'sectors', ['name'], unique=False)
    op.create_index(op.f('ix_sectors_tenant_id'), 'sectors', ['tenant_id'], unique=False)

    op.create_table('subscriptions',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('tenant_id', sa.UUID(), nullable=False),
        sa.Column('plan_id', sa.UUID(), nullable=False),
        sa.Column('status', sa.Enum('ACTIVE', 'PAST_DUE', 'CANCELED', 'EXPIRED', name='subscriptionstatus'), nullable=False),
        sa.Column('current_period_start', sa.DateTime(timezone=True), nullable=True),
        sa.Column('current_period_end', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['plan_id'], ['plans.id'], ),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('tenant_id')
    )

    op.create_table('users',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('tenant_id', sa.UUID(), nullable=True),
        sa.Column('email', sa.String(length=100), nullable=False),
        sa.Column('hashed_password', sa.String(length=255), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('tfa_secret', sa.String(length=255), nullable=True),
        sa.Column('is_tfa_enabled', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    # ### FASE 4: Tablas que dependen de USERS, ROLES, SECTORS, etc. ###
    op.create_table('assets',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('tenant_id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('serial_number', sa.String(length=100), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('asset_type_id', sa.UUID(), nullable=True),
        sa.Column('sector_id', sa.UUID(), nullable=True),
        sa.Column('properties', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['asset_type_id'], ['asset_types.id'], ),
        sa.ForeignKeyConstraint(['sector_id'], ['sectors.id'], ),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_assets_sector_id'), 'assets', ['sector_id'], unique=False)
    op.create_index(op.f('ix_assets_serial_number'), 'assets', ['serial_number'], unique=True)
    op.create_index(op.f('ix_assets_status'), 'assets', ['status'], unique=False)

    op.create_table('role_permissions',
        sa.Column('role_id', sa.UUID(), nullable=False),
        sa.Column('permission_id', sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(['permission_id'], ['permissions.id'], ),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
        sa.PrimaryKeyConstraint('role_id', 'permission_id')
    )

    op.create_table('user_roles',
        sa.Column('user_id', sa.UUID(), nullable=False),
        sa.Column('role_id', sa.UUID(), nullable=False),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('user_id', 'role_id')
    )
    
    op.create_table('audit_logs',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('tenant_id', sa.UUID(), nullable=False),
        sa.Column('user_id', sa.UUID(), nullable=True),
        sa.Column('action', sa.String(length=100), nullable=False),
        sa.Column('entity_type', sa.String(length=50), nullable=True),
        sa.Column('entity_id', sa.String(length=255), nullable=True),
        sa.Column('details', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_audit_logs_action'), 'audit_logs', ['action'], unique=False)
    op.create_index(op.f('ix_audit_logs_entity_id'), 'audit_logs', ['entity_id'], unique=False)
    op.create_index(op.f('ix_audit_logs_entity_type'), 'audit_logs', ['entity_type'], unique=False)
    op.create_index(op.f('ix_audit_logs_timestamp'), 'audit_logs', ['timestamp'], unique=False)
    op.create_index(op.f('ix_audit_logs_user_id'), 'audit_logs', ['user_id'], unique=False)

    # ### FASE 5: Tablas que dependen de ASSETS, USERS, etc. ###
    op.create_table('alarm_rules',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('asset_id', sa.UUID(), nullable=False),
        sa.Column('metric_name', sa.String(), nullable=False),
        sa.Column('condition', sa.String(), nullable=False),
        sa.Column('threshold', sa.Float(), nullable=False),
        sa.Column('severity', sa.String(), nullable=False),
        sa.Column('is_enabled', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['asset_id'], ['assets.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_alarm_rules_asset_id'), 'alarm_rules', ['asset_id'], unique=False)

    op.create_table('sensor_readings',
        sa.Column('timestamp', sa.DateTime(timezone=True), nullable=False),
        sa.Column('asset_id', sa.UUID(), nullable=False),
        sa.Column('metric_name', sa.String(), nullable=False),
        sa.Column('value', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(['asset_id'], ['assets.id'], ),
        sa.PrimaryKeyConstraint('timestamp', 'asset_id', 'metric_name')
    )
    op.create_index(op.f('ix_sensor_readings_metric_name'), 'sensor_readings', ['metric_name'], unique=False)
    op.create_index(op.f('ix_sensor_readings_timestamp'), 'sensor_readings', ['timestamp'], unique=False)

    op.create_table('work_orders',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('tenant_id', sa.UUID(), nullable=False),
        sa.Column('asset_id', sa.UUID(), nullable=False),
        sa.Column('category', sa.String(length=50), nullable=False),
        sa.Column('source_trigger', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False),
        sa.Column('priority', sa.String(length=50), nullable=False),
        sa.Column('title', sa.String(length=255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('due_date', sa.Date(), nullable=True),
        sa.Column('cancellation_reason', sa.Text(), nullable=True),
        sa.Column('rating', sa.Integer(), nullable=True),
        sa.Column('feedback', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('completed_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['asset_id'], ['assets.id'], ),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_work_orders_asset_id'), 'work_orders', ['asset_id'], unique=False)
    op.create_index(op.f('ix_work_orders_category'), 'work_orders', ['category'], unique=False)
    op.create_index(op.f('ix_work_orders_priority'), 'work_orders', ['priority'], unique=False)
    op.create_index(op.f('ix_work_orders_status'), 'work_orders', ['status'], unique=False)
    op.create_index(op.f('ix_work_orders_tenant_id'), 'work_orders', ['tenant_id'], unique=False)

    # ### FASE 6: Tablas finales con múltiples dependencias ###
    op.create_table('alarms',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('asset_id', sa.UUID(), nullable=False),
        sa.Column('alarm_rule_id', sa.UUID(), nullable=False),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('severity', sa.String(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('triggering_value', sa.Float(), nullable=True),
        sa.Column('acknowledged_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('acknowledged_by_id', sa.UUID(), nullable=True),
        sa.ForeignKeyConstraint(['alarm_rule_id'], ['alarm_rules.id'], ),
        sa.ForeignKeyConstraint(['asset_id'], ['assets.id'], ),
        sa.ForeignKeyConstraint(['acknowledged_by_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_alarms_alarm_rule_id'), 'alarms', ['alarm_rule_id'], unique=False)
    op.create_index(op.f('ix_alarms_asset_id'), 'alarms', ['asset_id'], unique=False)

    # --- TimescaleDB Hypertable y Políticas de Compresión ---
    op.execute("SELECT create_hypertable('sensor_readings', 'timestamp');")
    
    op.execute("""
        ALTER TABLE sensor_readings 
        SET (timescaledb.compress, timescaledb.compress_segmentby = 'asset_id');
    """)
    
    op.execute("""
        SELECT add_compression_policy('sensor_readings', INTERVAL '7 days');
    """)
    # ### end Alembic commands ###


def downgrade() -> None:
    # El downgrade de una migración maestra es destructivo y complejo.
    # Para un entorno de desarrollo, es más fácil destruir y recrear la BD.
    pass
