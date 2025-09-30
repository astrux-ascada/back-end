"""Add sector and properties to asset model

Revision ID: 0009
Revises: 0008
Create Date: 2024-07-19 12:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB


# revision identifiers, used by Alembic.
revision = '0009'
down_revision = '0008'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### Add sector_id column to assets table ###
    op.add_column('assets', sa.Column('sector_id', UUID(as_uuid=True), nullable=True))
    op.create_index(op.f('ix_assets_sector_id'), 'assets', ['sector_id'], unique=False)
    op.create_foreign_key(
        'assets_sector_id_fkey',
        'assets',
        'sectors',
        ['sector_id'],
        ['id']
    )

    # ### Add properties column to assets table ###
    op.add_column('assets', sa.Column('properties', JSONB(), nullable=True, comment='Propiedades específicas del activo en formato JSON.'))


def downgrade() -> None:
    # ### Revert properties column ###
    op.drop_column('assets', 'properties')

    # ### Revert sector_id column ###
    op.drop_constraint('assets_sector_id_fkey', 'assets', type_='foreignkey')
    op.drop_index(op.f('ix_assets_sector_id'), table_name='assets')
    op.drop_column('assets', 'sector_id')
