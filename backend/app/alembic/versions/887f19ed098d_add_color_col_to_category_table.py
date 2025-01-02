"""Add color col to category table

Revision ID: 887f19ed098d
Revises: 05d2137efd99
Create Date: 2025-01-02 16:25:18.307230

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '887f19ed098d'
down_revision = '05d2137efd99'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('category', sa.Column('color', sqlmodel.sql.sqltypes.AutoString(), nullable=False))
    op.create_unique_constraint(None, 'category', ['color'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'category', type_='unique')
    op.drop_column('category', 'color')
    # ### end Alembic commands ###