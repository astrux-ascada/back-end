"""Crea las tablas del módulo de activos

Revision ID: 0003
Revises: 0002
Create Date: 2024-07-18 14:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid


# revision identifiers, used by Alembic.
revision = '0003'
down_revision = '0002'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### AssetType Table ###
    op.create_table('asset_types',
    sa.Column('id', UUID(as_uuid=True), nullable=False, default=uuid.uuid4),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('manufacturer', sa.String(length=100), nullable=True),
    sa.Column('model_number', sa.String(length=100), nullable=True),
    sa.Column('category', sa.String(length=50), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_asset_types_name'), 'asset_types', ['name'], unique=True)
    op.create_index(op.f('ix_asset_types_category'), 'asset_types', ['category'], unique=False)

    # ### Asset Table ###
    op.create_table('assets',
    sa.Column('id', UUID(as_uuid=True), nullable=False, default=uuid.uuid4),
    sa.Column('asset_type_id', UUID(as_uuid=True), nullable=False),
    sa.Column('serial_number', sa.String(length=100), nullable=True),
    sa.Column('location', sa.String(length=150), nullable=True),
    sa.Column('status', sa.String(length=50), nullable=False, default='operational'),
    sa.Column('installed_at', sa.Date(), nullable=True),
    sa.Column('last_maintenance_at', sa.Date(), nullable=True),
    sa.Column('warranty_expires_at', sa.Date(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['asset_type_id'], ['asset_types.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_assets_serial_number'), 'assets', ['serial_number'], unique=True)
    op.create_index(op.f('ix_assets_status'), 'assets', ['status'], unique=False)

    # ### AssetHierarchy Table ###
    op.create_table('asset_hierarchy',
    sa.Column('parent_asset_type_id', UUID(as_uuid=True), nullable=False),
    sa.Column('child_asset_type_id', UUID(as_uuid=True), nullable=False),
    sa.Column('quantity', sa.Integer(), nullable=False, default=1),
    sa.ForeignKeyConstraint(['child_asset_type_id'], ['asset_types.id'], ),
    sa.ForeignKeyConstraint(['parent_asset_type_id'], ['asset_types.id'], ),
    sa.PrimaryKeyConstraint('parent_asset_type_id', 'child_asset_type_id')
    )


def downgrade() -> None:
    op.drop_table('asset_hierarchy')
    op.drop_index(op.f('ix_assets_status'), table_name='assets')
    op.drop_index(op.f('ix_assets_serial_number'), table_name='assets')
    op.drop_table('assets')
    op.drop_index(op.f('ix_asset_types_category'), table_name='asset_types')
    op.drop_index(op.f('ix_asset_types_name'), table_name='asset_types')
    op.drop_table('asset_types')
