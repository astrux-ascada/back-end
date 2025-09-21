"""Crea la extensión de TimescaleDB en la base de datos.

Revision ID: 0001
Revises: 
Create Date: 2024-07-17 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0001'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    """Aplica la migración, creando la extensión de TimescaleDB."""
    op.execute("CREATE EXTENSION IF NOT EXISTS timescaledb;")


def downgrade() -> None:
    """Revierte la migración, eliminando la extensión de TimescaleDB."""
    op.execute("DROP EXTENSION timescaledb;")
