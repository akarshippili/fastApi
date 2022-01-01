"""add created_at and publish columns to post table

Revision ID: ef03f51aba74
Revises: c9b5c46cf3de
Create Date: 2022-01-01 20:21:58.119755

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ef03f51aba74'
down_revision = 'c9b5c46cf3de'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(
        timezone=True), nullable=False, server_default=sa.text('now()')))
    op.add_column('posts', sa.Column('published', sa.Boolean(),
                  server_default='TRUE', nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'created_at')
    op.drop_column('posts', 'published')
    pass
