"""Create configuration tables

Revision ID: 0011
Revises: 0010
Create Date: 2024-07-21 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = '0011'
down_revision = '0010'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### Create configuration_parameters table ###
    op.create_table(
        'configuration_parameters',
        sa.Column('key', sa.String(length=255), nullable=False),
        sa.Column('value', sa.Text(), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('is_editable', sa.Boolean(), nullable=False, default=True),
        sa.PrimaryKeyConstraint('key')
    )
    op.create_index(op.f('ix_configuration_parameters_key'), 'configuration_parameters', ['key'], unique=True)

    # ### Create enum_types table ###
    op.create_table(
        'enum_types',
        sa.Column('id', UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False, comment='Ej: WorkOrderStatus, AssetStatus'),
        sa.Column('description', sa.Text(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_enum_types_name'), 'enum_types', ['name'], unique=True)

    # ### Create enum_values table ###
    op.create_table(
        'enum_values',
        sa.Column('id', UUID(as_uuid=True), nullable=False),
        sa.Column('enum_type_id', UUID(as_uuid=True), nullable=False),
        sa.Column('value', sa.String(length=100), nullable=False, comment='El valor real, ej: IN_PROGRESS'),
        sa.Column('label', sa.String(length=150), nullable=False, comment='La etiqueta para la UI, ej: En Progreso'),
        sa.Column('color', sa.String(length=20), nullable=True, comment='Un color opcional para la UI, ej: #3b82f6'),
        sa.ForeignKeyConstraint(['enum_type_id'], ['enum_types.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_enum_values_enum_type_id'), 'enum_values', ['enum_type_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_enum_values_enum_type_id'), table_name='enum_values')
    op.drop_table('enum_values')
    op.drop_index(op.f('ix_enum_types_name'), table_name='enum_types')
    op.drop_table('enum_types')
    op.drop_index(op.f('ix_configuration_parameters_key'), table_name='configuration_parameters')
    op.drop_table('configuration_parameters')
