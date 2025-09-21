"""Crea las tablas del módulo de compras (procurement)

Revision ID: 0005
Revises: 0004
Create Date: 2024-07-18 16:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid


# revision identifiers, used by Alembic.
revision = '0005'
down_revision = '0004'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### Provider Table ###
    op.create_table('providers',
    sa.Column('id', UUID(as_uuid=True), nullable=False, default=uuid.uuid4),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('contact_info', sa.String(length=255), nullable=True, comment='Email, phone, or address of the provider.'),
    sa.Column('specialty', sa.String(length=100), nullable=True, comment='Area of expertise, e.g., Robotics, HVAC, PLC Programming.'),
    sa.Column('performance_score', sa.Float(), nullable=True, comment='A score from 0-100 representing provider performance.'),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_providers_name'), 'providers', ['name'], unique=True)
    op.create_index(op.f('ix_providers_specialty'), 'providers', ['specialty'], unique=False)
    op.create_index(op.f('ix_providers_performance_score'), 'providers', ['performance_score'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_providers_performance_score'), table_name='providers')
    op.drop_index(op.f('ix_providers_specialty'), table_name='providers')
    op.drop_index(op.f('ix_providers_name'), table_name='providers')
    op.drop_table('providers')
