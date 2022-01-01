"""create post table

Revision ID: 75f5cab8fbf9
Revises: 
Create Date: 2022-01-01 19:47:21.403214

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '75f5cab8fbf9'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('posts',
                    sa.Column('id', sa.Integer(),
                              primary_key=True, nullable=False),
                    sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_table('posts')
    pass
