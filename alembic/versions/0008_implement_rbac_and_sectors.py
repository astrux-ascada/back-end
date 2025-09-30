"""Implementa el modelo RBAC granular y los Sectores

Revision ID: 0008
Revises: 0007
Create Date: 2024-07-19 10:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import UUID
import uuid


# revision identifiers, used by Alembic.
revision = '0008'
down_revision = '0007'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### Fase A: Implementar RBAC Granular ###

    # 1. Crear tabla `permissions`
    op.create_table('permissions',
    sa.Column('id', UUID(as_uuid=True), nullable=False, default=uuid.uuid4),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_permissions_name'), 'permissions', ['name'], unique=True)

    # 2. Crear tabla de asociación `role_permissions`
    op.create_table('role_permissions',
    sa.Column('role_id', UUID(as_uuid=True), nullable=False),
    sa.Column('permission_id', UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['permission_id'], ['permissions.id'], ),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.PrimaryKeyConstraint('role_id', 'permission_id')
    )

    # 3. Crear tabla de asociación `user_roles`
    op.create_table('user_roles',
    sa.Column('user_id', UUID(as_uuid=True), nullable=False),
    sa.Column('role_id', UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'role_id')
    )

    # 4. Modificar tabla `users` para eliminar la antigua relación
    op.drop_constraint('users_role_id_fkey', 'users', type_='foreignkey')
    op.drop_column('users', 'role_id')

    # ### Fase B: Implementar Sectores ###

    # 5. Crear tabla `sectors`
    op.create_table('sectors',
    sa.Column('id', UUID(as_uuid=True), nullable=False, default=uuid.uuid4),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('description', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_sectors_name'), 'sectors', ['name'], unique=True)

    # 6. Crear tabla de asociación `user_sectors`
    op.create_table('user_sectors',
    sa.Column('user_id', UUID(as_uuid=True), nullable=False),
    sa.Column('sector_id', UUID(as_uuid=True), nullable=False),
    sa.ForeignKeyConstraint(['sector_id'], ['sectors.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('user_id', 'sector_id')
    )


def downgrade() -> None:
    # Revertir en orden inverso para evitar problemas de claves foráneas
    op.drop_table('user_sectors')
    op.drop_index(op.f('ix_sectors_name'), table_name='sectors')
    op.drop_table('sectors')
    
    op.add_column('users', sa.Column('role_id', UUID(as_uuid=True), autoincrement=False, nullable=True))
    op.create_foreign_key('users_role_id_fkey', 'users', 'roles', ['role_id'], ['id'])
    
    op.drop_table('user_roles')
    op.drop_table('role_permissions')
    op.drop_index(op.f('ix_permissions_name'), table_name='permissions')
    op.drop_table('permissions')
