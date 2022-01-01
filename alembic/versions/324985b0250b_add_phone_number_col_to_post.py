"""add phone_number col to post

Revision ID: 324985b0250b
Revises: 52eebf682f71
Create Date: 2022-01-01 20:35:23.009172

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '324985b0250b'
down_revision = '52eebf682f71'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('posts', sa.Column('phone_number', sa.String(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('posts', 'phone_number')
    # ### end Alembic commands ###
