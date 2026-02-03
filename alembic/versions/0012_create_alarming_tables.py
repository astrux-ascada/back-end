"""Create alarming tables

Revision ID: 0012
Revises: 0011
Create Date: 2024-07-22 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID


# revision identifiers, used by Alembic.
revision = '0012'
down_revision = '0011'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### Create alarm_rules table ###
    op.create_table(
        'alarm_rules',
        sa.Column('id', UUID(as_uuid=True), nullable=False),
        sa.Column('asset_id', UUID(as_uuid=True), nullable=False),
        sa.Column('metric_name', sa.String(length=100), nullable=False),
        sa.Column('condition', sa.String(length=10), nullable=False),
        sa.Column('threshold', sa.Float(), nullable=False),
        sa.Column('severity', sa.String(length=50), nullable=False),
        sa.Column('is_enabled', sa.Boolean(), nullable=False, default=True),
        sa.ForeignKeyConstraint(['asset_id'], ['assets.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_alarm_rules_asset_id'), 'alarm_rules', ['asset_id'], unique=False)
    op.create_index(op.f('ix_alarm_rules_metric_name'), 'alarm_rules', ['metric_name'], unique=False)
    op.create_index(op.f('ix_alarm_rules_is_enabled'), 'alarm_rules', ['is_enabled'], unique=False)

    # ### Create alarms table ###
    op.create_table(
        'alarms',
        sa.Column('id', UUID(as_uuid=True), nullable=False),
        sa.Column('rule_id', UUID(as_uuid=True), nullable=False),
        sa.Column('triggered_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('acknowledged_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('cleared_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=False, default='ACTIVE'),
        sa.Column('triggering_value', sa.Float(), nullable=False),
        sa.ForeignKeyConstraint(['rule_id'], ['alarm_rules.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_alarms_rule_id'), 'alarms', ['rule_id'], unique=False)
    op.create_index(op.f('ix_alarms_status'), 'alarms', ['status'], unique=False)
    op.create_index(op.f('ix_alarms_triggered_at'), 'alarms', ['triggered_at'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_alarms_triggered_at'), table_name='alarms')
    op.drop_index(op.f('ix_alarms_status'), table_name='alarms')
    op.drop_index(op.f('ix_alarms_rule_id'), table_name='alarms')
    op.drop_table('alarms')
    op.drop_index(op.f('ix_alarm_rules_is_enabled'), table_name='alarm_rules')
    op.drop_index(op.f('ix_alarm_rules_metric_name'), table_name='alarm_rules')
    op.drop_index(op.f('ix_alarm_rules_asset_id'), table_name='alarm_rules')
    op.drop_table('alarm_rules')
