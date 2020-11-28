"""empty message

Revision ID: 8c6e689cf7dd
Revises: 3254fb588813
Create Date: 2020-05-08 21:55:21.974144

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = '8c6e689cf7dd'
down_revision = '3254fb588813'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cms_user', sa.Column('_password', sa.String(length=100), nullable=False))
    op.drop_column('cms_user', 'password')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cms_user', sa.Column('password', mysql.VARCHAR(length=50), nullable=False))
    op.drop_column('cms_user', '_password')
    # ### end Alembic commands ###
