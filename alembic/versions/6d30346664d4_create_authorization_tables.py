"""create authorization tables

Revision ID: 6d30346664d4
Revises: 872e22259aa3
Create Date: 2022-11-03 11:41:58.417597

"""
from alembic import op
from datetime import datetime
import sqlalchemy as sa
from uuid import uuid4
from passlib.context import CryptContext

from src.database.settings import GUID


# revision identifiers, used by Alembic.
revision = '6d30346664d4'
down_revision = '872e22259aa3'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'roles',
        sa.Column(
            'uuid',
            GUID(),
            primary_key=True,
            index=True,
            default=uuid4,
            unique=True
        ),
        sa.Column('created_at', sa.DateTime, default=datetime.now()),
        sa.Column('updated_at', sa.DateTime, nullable=True, default=None),
        sa.Column('name', sa.String, nullable=False, unique=True),
        sa.Column('deletable', sa.Boolean, default=True)
    )

    op.create_table(
        'entities',
        sa.Column(
            'uuid',
            GUID(),
            primary_key=True,
            index=True,
            default=uuid4,
            unique=True
        ),
        sa.Column('created_at', sa.DateTime, default=datetime.now()),
        sa.Column('updated_at', sa.DateTime, nullable=True, default=None),
        sa.Column('name', sa.String, nullable=False, unique=True)
    )

    op.create_table(
        'role_entity',
        sa.Column('created_at', sa.DateTime, default=datetime.now()),
        sa.Column('updated_at', sa.DateTime, nullable=True, default=None),
        sa.Column('entity_uuid', GUID(), sa.ForeignKey('entities.uuid'), primary_key=True, index=True),
        sa.Column('role_uuid', GUID(), sa.ForeignKey('roles.uuid'), primary_key=True, index=True),
        sa.Column('can_read', sa.Boolean, default=True),
        sa.Column('can_write', sa.Boolean, default=False)
    )

    op.add_column(
        'users',
        sa.Column('role_uuid', GUID(), sa.ForeignKey('roles.uuid'), index=True, nullable=True)
    )

    # Entities register
    sql_entities = f'''
        INSERT INTO entities(uuid, created_at, name) VALUES
        ('{uuid4()}', '{datetime.now()}', 'roles'),
        ('{uuid4()}', '{datetime.now()}', 'entities'),
        ('{uuid4()}', '{datetime.now()}', 'permissions'),
        ('{uuid4()}', '{datetime.now()}', 'users');
    '''
    op.execute(sql_entities)

    admin_uuid = uuid4()
    sql_roles = f'''
        INSERT INTO roles(uuid, name, deletable, created_at)
        VALUES('{admin_uuid}', 'Admin', FALSE, '{datetime.now()}');
    '''
    op.execute(sql_roles)

    user_uuid = uuid4()
    sql_user = f'''
        INSERT INTO users(uuid, role_uuid, name, created_at) VALUES
        ('{user_uuid}', '{admin_uuid}', 'Admin', '{datetime.now()}');
    '''

    op.execute(sql_user)

    pwd_context = CryptContext(schemes=["sha256_crypt"], deprecated="auto")
    password = pwd_context.hash('pass123')
    sql_auth = f'''
        INSERT INTO auth(email, password, active, user_uuid, created_at) VALUES
        ('admin@admin.com', '{password}', TRUE, '{user_uuid}', '{datetime.now()}');
    '''
    op.execute(sql_auth)


def downgrade() -> None:
    op.execute('DELETE FROM auth')
    op.execute('DELETE FROM users')
    op.execute('DELETE FROM roles')
    op.execute('DELETE FROM entities')

    op.drop_column('users', 'role_uuid')
    op.drop_table('role_entity')
    op.drop_table('entities')
    op.drop_table('roles')
