"""Crea la hypertable para las lecturas de sensores

Revision ID: 0004
Revises: 0003
Create Date: 2024-07-18 15:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = '0004'
down_revision = '0003'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### Paso 1: Crear la tabla estándar ###
    op.create_table('sensor_readings',
    sa.Column('timestamp', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.Column('asset_id', UUID(as_uuid=True), nullable=False),
    sa.Column('metric_name', sa.String(length=100), nullable=False),
    sa.Column('value', sa.Float(), nullable=False),
    sa.ForeignKeyConstraint(['asset_id'], ['assets.id'], ),
    sa.PrimaryKeyConstraint('timestamp', 'asset_id')
    )
    op.create_index(op.f('ix_sensor_readings_asset_id'), 'sensor_readings', ['asset_id'], unique=False)
    op.create_index(op.f('ix_sensor_readings_metric_name'), 'sensor_readings', ['metric_name'], unique=False)
    op.create_index(op.f('ix_sensor_readings_timestamp'), 'sensor_readings', ['timestamp'], unique=False)

    # ### Paso 2: Convertir la tabla en una Hypertable de TimescaleDB ###
    # Este es el comando mágico que optimiza la tabla para series temporales.
    op.execute("SELECT create_hypertable('sensor_readings', 'timestamp');")


def downgrade() -> None:
    # El downgrade simplemente elimina la tabla. TimescaleDB maneja la eliminación de la hypertable.
    op.drop_index(op.f('ix_sensor_readings_timestamp'), table_name='sensor_readings')
    op.drop_index(op.f('ix_sensor_readings_metric_name'), table_name='sensor_readings')
    op.drop_index(op.f('ix_sensor_readings_asset_id'), table_name='sensor_readings')
    op.drop_table('sensor_readings')
