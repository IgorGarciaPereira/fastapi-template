"""create users table

Revision ID: 14ef828bb610
Revises: 
Create Date: 2022-10-31 18:04:08.308884

"""
from datetime import datetime
from uuid import uuid4

from alembic import op
import sqlalchemy as sa

from src.database.settings import GUID

# revision identifiers, used by Alembic.
revision = '14ef828bb610'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'users',
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
        sa.Column('name', sa.String),
        sa.Column('surname', sa.String)
    )


def downgrade() -> None:
    op.drop_table('users')
