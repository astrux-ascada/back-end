"""Crea las tablas del módulo de mantenimiento

Revision ID: 0006
Revises: 0005
Create Date: 2024-07-18 17:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID, JSONB
import uuid


# revision identifiers, used by Alembic.
revision = '0006'
down_revision = '0005'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### WorkOrder Table ###
    op.create_table('work_orders',
    sa.Column('id', UUID(as_uuid=True), nullable=False, default=uuid.uuid4),
    sa.Column('asset_id', UUID(as_uuid=True), nullable=False),
    sa.Column('category', sa.String(length=50), nullable=False, comment='CORRECTIVE, PREVENTIVE, PREDICTIVE, IMPROVEMENT'),
    sa.Column('source_trigger', JSONB(), nullable=True, comment='JSON data explaining the origin of the work order.'),
    sa.Column('status', sa.String(length=50), nullable=False, default='OPEN', comment='OPEN, IN_PROGRESS, ON_HOLD, COMPLETED, CANCELED'),
    sa.Column('priority', sa.String(length=50), nullable=False, default='MEDIUM', comment='LOW, MEDIUM, HIGH, URGENT'),
    sa.Column('summary', sa.String(length=255), nullable=False, comment='A brief, one-line summary of the work to be done.'),
    sa.Column('description', sa.Text(), nullable=True, comment='A detailed description of the issue and required work.'),
    sa.Column('due_date', sa.Date(), nullable=True),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('completed_at', sa.TIMESTAMP(timezone=True), nullable=True),
    sa.ForeignKeyConstraint(['asset_id'], ['assets.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_work_orders_asset_id'), 'work_orders', ['asset_id'], unique=False)
    op.create_index(op.f('ix_work_orders_category'), 'work_orders', ['category'], unique=False)
    op.create_index(op.f('ix_work_orders_status'), 'work_orders', ['status'], unique=False)
    op.create_index(op.f('ix_work_orders_priority'), 'work_orders', ['priority'], unique=False)

    # ### MaintenanceTask Table ###
    op.create_table('maintenance_tasks',
    sa.Column('id', UUID(as_uuid=True), nullable=False, default=uuid.uuid4),
    sa.Column('work_order_id', UUID(as_uuid=True), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=False, comment='Description of the specific task to be performed.'),
    sa.Column('order', sa.Integer(), nullable=True, default=1, comment='The sequence order of the task within the work order.'),
    sa.Column('is_completed', sa.Boolean(), nullable=False, default=False),
    sa.Column('created_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.Column('updated_at', sa.TIMESTAMP(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['work_order_id'], ['work_orders.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_maintenance_tasks_work_order_id'), 'maintenance_tasks', ['work_order_id'], unique=False)

    # ### WorkOrderUserAssignment Table ###
    op.create_table('work_order_user_assignments',
    sa.Column('work_order_id', UUID(as_uuid=True), nullable=False),
    sa.Column('user_id', UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['work_order_id'], ['work_orders.id'], ),
    sa.PrimaryKeyConstraint('work_order_id', 'user_id')
    )

    # ### WorkOrderProviderAssignment Table ###
    op.create_table('work_order_provider_assignments',
    sa.Column('work_order_id', UUID(as_uuid=True), nullable=False),
    sa.Column('provider_id', UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['provider_id'], ['providers.id'], ),
    sa.ForeignKeyConstraint(['work_order_id'], ['work_orders.id'], ),
    sa.PrimaryKeyConstraint('work_order_id', 'provider_id')
    )


def downgrade() -> None:
    op.drop_table('work_order_provider_assignments')
    op.drop_table('work_order_user_assignments')
    op.drop_index(op.f('ix_maintenance_tasks_work_order_id'), table_name='maintenance_tasks')
    op.drop_table('maintenance_tasks')
    op.drop_index(op.f('ix_work_orders_priority'), table_name='work_orders')
    op.drop_index(op.f('ix_work_orders_status'), table_name='work_orders')
    op.drop_index(op.f('ix_work_orders_category'), table_name='work_orders')
    op.drop_index(op.f('ix_work_orders_asset_id'), table_name='work_orders')
    op.drop_table('work_orders')
