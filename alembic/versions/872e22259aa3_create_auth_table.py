"""create auth table

Revision ID: 872e22259aa3
Revises: 14ef828bb610
Create Date: 2022-11-01 15:30:01.694151

"""
from alembic import op
import sqlalchemy as sa

from src.database.settings import GUID


# revision identifiers, used by Alembic.
revision = '872e22259aa3'
down_revision = '14ef828bb610'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'auth',
        sa.Column('email', sa.String, primary_key=True, index=True),
        sa.Column('password', sa.String, nullable=False),
        sa.Column('active', sa.Boolean, default=False),
        sa.Column('user_uuid', GUID(), sa.ForeignKey('users.uuid'))
    )


def downgrade() -> None:
    op.drop_table('auth')
