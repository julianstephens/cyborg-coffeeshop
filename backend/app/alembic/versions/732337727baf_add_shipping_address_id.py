"""Add shipping address id

Revision ID: 732337727baf
Revises: 6b595fb76cca
Create Date: 2025-01-04 01:09:01.379002

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '732337727baf'
down_revision = '6b595fb76cca'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('shipping_address_id', sa.Uuid(), nullable=True))
    op.create_foreign_key(None, 'order', 'address', ['shipping_address_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'order', type_='foreignkey')
    op.drop_column('order', 'shipping_address_id')
    # ### end Alembic commands ###
