"""Add images to product table

Revision ID: 78a9243d76b6
Revises: 887f19ed098d
Create Date: 2025-01-02 17:00:50.288723

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '78a9243d76b6'
down_revision = '887f19ed098d'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('images', sa.ARRAY(sa.String()), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('product', 'images')
    # ### end Alembic commands ###