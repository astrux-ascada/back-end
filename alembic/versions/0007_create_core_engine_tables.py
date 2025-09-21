"""Crea las tablas del módulo Core Engine

Revision ID: 0007
Revises: 0006
Create Date: 2024-07-18 18:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid


# revision identifiers, used by Alembic.
revision = '0007'
down_revision = '0006'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### DataSource Table ###
    op.create_table('data_sources',
    sa.Column('id', UUID(as_uuid=True), nullable=False, default=uuid.uuid4),
    sa.Column('name', sa.String(length=100), nullable=False, comment='Nombre descriptivo, ej: \'PLC Línea de Ensamblaje 3\''),
    sa.Column('protocol', sa.String(length=50), nullable=False, comment='Protocolo de comunicación, ej: \'OPCUA\', \'MODBUS_TCP\''),
    sa.Column('connection_params', JSONB(), nullable=False, comment='Ej: {"host": "192.168.1.10", "port": 4840, "security_mode": "SignAndEncrypt"}'),
    sa.Column('is_active', sa.Boolean(), nullable=False, default=False, comment='Habilita o deshabilita la recolección de datos de esta fuente.'),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_data_sources_name'), 'data_sources', ['name'], unique=True)
    op.create_index(op.f('ix_data_sources_protocol'), 'data_sources', ['protocol'], unique=False)
    op.create_index(op.f('ix_data_sources_is_active'), 'data_sources', ['is_active'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_data_sources_is_active'), table_name='data_sources')
    op.drop_index(op.f('ix_data_sources_protocol'), table_name='data_sources')
    op.drop_index(op.f('ix_data_sources_name'), table_name='data_sources')
    op.drop_table('data_sources')
