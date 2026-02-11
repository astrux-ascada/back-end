"""Add notification config tables

Revision ID: 6c9014591a0a
Revises: 4f5394da9ce3
Create Date: 2026-02-10 10:03:03.959727

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '6c9014591a0a'
down_revision: Union[str, None] = '4f5394da9ce3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

# Definición explícita de los NUEVOS tipos ENUM
notification_channel_type_enum = postgresql.ENUM('IN_APP', 'EMAIL', 'SMS', 'PUSH', name='notification_channel_type')
notification_recipient_type_enum = postgresql.ENUM('ROLE', 'USER', 'TENANT_ADMIN_OF_ENTITY', 'REQUESTER', name='notification_recipient_type')

def upgrade() -> None:
    # 1. Crear los NUEVOS tipos ENUM primero de forma segura
    notification_channel_type_enum.create(op.get_bind(), checkfirst=True)
    notification_recipient_type_enum.create(op.get_bind(), checkfirst=True)

    op.create_table('notification_channels',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        # Sintaxis CORRECTA: Usar postgresql.ENUM con create_type=False
        sa.Column('type', postgresql.ENUM('IN_APP', 'EMAIL', 'SMS', 'PUSH', name='notification_channel_type', create_type=False), nullable=False),
        sa.Column('config', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default='NOW()', nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default='NOW()', nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notification_channels_name'), 'notification_channels', ['name'], unique=True)
    
    op.create_table('notification_templates',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        # Sintaxis CORRECTA: create_type=False porque notification_level YA EXISTE
        sa.Column('level', postgresql.ENUM('TENANT', 'PLATFORM', name='notification_level', create_type=False), nullable=False),
        sa.Column('subject', sa.String(length=255), nullable=True),
        sa.Column('body', sa.Text(), nullable=False),
        sa.Column('placeholders', postgresql.JSONB(astext_type=sa.Text()), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default='NOW()', nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default='NOW()', nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notification_templates_name'), 'notification_templates', ['name'], unique=True)
    
    op.create_table('notification_rules',
        sa.Column('id', sa.UUID(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.Column('event_type', sa.String(length=100), nullable=False),
        sa.Column('template_id', sa.UUID(), nullable=False),
        sa.Column('channel_id', sa.UUID(), nullable=False),
        # Sintaxis CORRECTA
        sa.Column('recipient_type', postgresql.ENUM('ROLE', 'USER', 'TENANT_ADMIN_OF_ENTITY', 'REQUESTER', name='notification_recipient_type', create_type=False), nullable=False),
        sa.Column('recipient_id', sa.UUID(), nullable=True),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default='NOW()', nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), server_default='NOW()', nullable=False),
        sa.ForeignKeyConstraint(['channel_id'], ['notification_channels.id'], ),
        sa.ForeignKeyConstraint(['template_id'], ['notification_templates.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_notification_rules_event_type'), 'notification_rules', ['event_type'], unique=False)
    op.create_index(op.f('ix_notification_rules_name'), 'notification_rules', ['name'], unique=True)


def downgrade() -> None:
    op.drop_index(op.f('ix_notification_rules_name'), table_name='notification_rules')
    op.drop_index(op.f('ix_notification_rules_event_type'), table_name='notification_rules')
    op.drop_table('notification_rules')
    op.drop_index(op.f('ix_notification_templates_name'), table_name='notification_templates')
    op.drop_table('notification_templates')
    op.drop_index(op.f('ix_notification_channels_name'), table_name='notification_channels')
    op.drop_table('notification_channels')
    
    # Eliminar los NUEVOS tipos ENUM al final
    notification_channel_type_enum.drop(op.get_bind(), checkfirst=True)
    notification_recipient_type_enum.drop(op.get_bind(), checkfirst=True)
