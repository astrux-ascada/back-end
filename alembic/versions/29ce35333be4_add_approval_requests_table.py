"""add_approval_requests_table

Revision ID: 29ce35333be4
Revises: 62bdc06ef135
Create Date: 2026-02-03 08:15:14.189682

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '29ce35333be4'
down_revision: Union[str, None] = '62bdc06ef135'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### Comandos seguros para crear las nuevas tablas ###
    
    # 1. Crear tabla 'approval_requests'
    op.create_table('approval_requests',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('tenant_id', sa.UUID(), nullable=False),
        sa.Column('requester_id', sa.UUID(), nullable=False),
        sa.Column('approver_id', sa.UUID(), nullable=True),
        sa.Column('entity_type', sa.String(length=50), nullable=False, comment='Ej: ASSET, WORK_ORDER'),
        sa.Column('entity_id', sa.UUID(), nullable=False),
        sa.Column('action', sa.String(length=50), nullable=False, comment='Ej: DELETE, ARCHIVE'),
        sa.Column('payload', sa.JSON(), nullable=True),
        sa.Column('status', sa.String(length=20), nullable=False),
        sa.Column('request_justification', sa.String(length=500), nullable=False),
        sa.Column('rejection_reason', sa.String(length=500), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('responded_at', sa.DateTime(timezone=True), nullable=True),
        sa.ForeignKeyConstraint(['approver_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['requester_id'], ['users.id'], ),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_approval_requests_entity_id'), 'approval_requests', ['entity_id'], unique=False)
    op.create_index(op.f('ix_approval_requests_entity_type'), 'approval_requests', ['entity_type'], unique=False)
    op.create_index(op.f('ix_approval_requests_status'), 'approval_requests', ['status'], unique=False)
    op.create_index(op.f('ix_approval_requests_tenant_id'), 'approval_requests', ['tenant_id'], unique=False)

    # 2. Crear tabla 'media_items'
    op.create_table('media_items',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('tenant_id', sa.UUID(), nullable=False),
        sa.Column('uploaded_by_id', sa.UUID(), nullable=False),
        sa.Column('context', sa.String(length=100), nullable=False),
        sa.Column('context_id', sa.UUID(), nullable=True),
        sa.Column('file_path', sa.String(length=1024), nullable=False),
        sa.Column('original_filename', sa.String(length=255), nullable=False),
        sa.Column('content_type', sa.String(length=100), nullable=False),
        sa.Column('size_bytes', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
        sa.ForeignKeyConstraint(['tenant_id'], ['tenants.id'], ),
        sa.ForeignKeyConstraint(['uploaded_by_id'], ['users.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('file_path')
    )
    op.create_index(op.f('ix_media_items_context'), 'media_items', ['context'], unique=False)
    op.create_index(op.f('ix_media_items_context_id'), 'media_items', ['context_id'], unique=False)
    op.create_index(op.f('ix_media_items_tenant_id'), 'media_items', ['tenant_id'], unique=False)


def downgrade() -> None:
    # ### Comandos para revertir la creación de las nuevas tablas ###
    op.drop_index(op.f('ix_media_items_tenant_id'), table_name='media_items')
    op.drop_index(op.f('ix_media_items_context_id'), table_name='media_items')
    op.drop_index(op.f('ix_media_items_context'), table_name='media_items')
    op.drop_table('media_items')
    
    op.drop_index(op.f('ix_approval_requests_tenant_id'), table_name='approval_requests')
    op.drop_index(op.f('ix_approval_requests_status'), table_name='approval_requests')
    op.drop_index(op.f('ix_approval_requests_entity_type'), table_name='approval_requests')
    op.drop_index(op.f('ix_approval_requests_entity_id'), table_name='approval_requests')
    op.drop_table('approval_requests')
