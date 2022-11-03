"""create authorization tables

Revision ID: 6d30346664d4
Revises: 872e22259aa3
Create Date: 2022-11-03 11:41:58.417597

"""
from alembic import op
from datetime import datetime
import sqlalchemy as sa
from uuid import uuid4

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
        sa.Column('name', sa.String, nullable=False),
        sa.Column('deletable', sa.Boolean, default=True)
    )

    op.create_table(
        'permissions',
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
        sa.Column('name', sa.String, nullable=False)
    )

    op.create_table(
        'role_permissions',
        sa.Column('created_at', sa.DateTime, default=datetime.now()),
        sa.Column('updated_at', sa.DateTime, nullable=True, default=None),
        sa.Column('permission_uuid', GUID(), sa.ForeignKey('permissions.uuid'), primary_key=True, index=True),
        sa.Column('role_uuid', GUID(), sa.ForeignKey('roles.uuid'), primary_key=True, index=True),
        sa.Column('can_read', sa.Boolean, default=True),
        sa.Column('can_write', sa.Boolean, default=False)
    )


def downgrade() -> None:
    op.drop_table('role_permissions')
    op.drop_table('permissions')
    op.drop_table('roles')
