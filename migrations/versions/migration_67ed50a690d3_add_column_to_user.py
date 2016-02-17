"""add column to user

Revision ID: 67ed50a690d3
Revises: None
Create Date: 2016-02-17 12:47:41.990550

"""

# revision identifiers, used by Alembic.
revision = '67ed50a690d3'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.add_column('user', sa.Column('is_active', sa.Boolean(), nullable=True))


def downgrade():
    pass
