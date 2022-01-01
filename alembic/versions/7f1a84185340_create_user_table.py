"""create user table

Revision ID: 7f1a84185340
Revises: ea5b31d9feb0
Create Date: 2022-01-01 20:08:14.735703

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql.schema import UniqueConstraint


# revision identifiers, used by Alembic.
revision = '7f1a84185340'
down_revision = 'ea5b31d9feb0'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('users',
                    sa.Column('id', sa.Integer(), nullable=False),
                    sa.Column('email', sa.String(), nullable=False),
                    sa.Column('password', sa.String(), nullable=False),
                    sa.Column('created_at', sa.TIMESTAMP(timezone=True),
                              nullable=False, server_default=sa.text('now()')),
                    sa.PrimaryKeyConstraint('id'),
                    sa.UniqueConstraint('email'))
    pass


def downgrade():
    op.drop_table('users')
    pass
