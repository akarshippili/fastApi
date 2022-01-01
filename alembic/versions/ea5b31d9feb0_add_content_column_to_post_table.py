"""add content column to post table

Revision ID: ea5b31d9feb0
Revises: 75f5cab8fbf9
Create Date: 2022-01-01 19:59:00.411418

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ea5b31d9feb0'
down_revision = '75f5cab8fbf9'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))


def downgrade():
    op.drop_column('posts', 'content')
