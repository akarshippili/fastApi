"""add fk_post_user to post table

Revision ID: c9b5c46cf3de
Revises: 7f1a84185340
Create Date: 2022-01-01 20:16:12.391231

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c9b5c46cf3de'
down_revision = '7f1a84185340'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('fk_post_user', source_table='posts', referent_table='users', local_cols=[
                          'owner_id'], remote_cols=['id'], ondelete='CASCADE')
    pass


def downgrade():
    op.drop_constraint('fk_post_user', 'posts', type_='foreignkey')
    op.drop_column('posts', 'owner_id')
    pass
