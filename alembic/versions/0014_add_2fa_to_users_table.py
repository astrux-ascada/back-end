"""Add 2FA fields to users table

Revision ID: 0014
Revises: 0013
Create Date: 2024-07-24 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0014'
down_revision = '0013'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### Add 2FA columns to users table ###
    op.add_column('users', sa.Column('tfa_secret', sa.String(length=255), nullable=True, comment='Secreto para la autenticación de dos factores (2FA).'))
    op.add_column('users', sa.Column('is_tfa_enabled', sa.Boolean(), nullable=False, server_default=sa.text('false'), comment='Indica si el 2FA está habilitado para el usuario.'))


def downgrade() -> None:
    # ### Drop 2FA columns from users table ###
    op.drop_column('users', 'is_tfa_enabled')
    op.drop_column('users', 'tfa_secret')
