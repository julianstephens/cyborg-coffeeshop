"""Add orderaddress link table

Revision ID: 4ba1c09f9700
Revises: eccc5e157037
Create Date: 2025-01-03 14:32:01.286513

"""
from alembic import op
import sqlalchemy as sa
import sqlmodel.sql.sqltypes


# revision identifiers, used by Alembic.
revision = '4ba1c09f9700'
down_revision = 'eccc5e157037'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('orderaddresslink',
    sa.Column('id', sa.Uuid(), nullable=False),
    sa.Column('created_at', sa.Integer(), nullable=False),
    sa.Column('updated_at', sa.Integer(), nullable=True),
    sa.Column('order_id', sa.Uuid(), nullable=False),
    sa.Column('address_id', sa.Uuid(), nullable=False),
    sa.ForeignKeyConstraint(['address_id'], ['address.id'], ),
    sa.ForeignKeyConstraint(['order_id'], ['order.id'], ),
    sa.PrimaryKeyConstraint('id', 'order_id', 'address_id')
    )
    op.drop_constraint('order_billing_address_id_fkey', 'order', type_='foreignkey')
    op.drop_constraint('order_shipping_address_id_fkey', 'order', type_='foreignkey')
    op.drop_column('order', 'billing_address_id')
    op.drop_column('order', 'shipping_address_id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('order', sa.Column('shipping_address_id', sa.UUID(), autoincrement=False, nullable=True))
    op.add_column('order', sa.Column('billing_address_id', sa.UUID(), autoincrement=False, nullable=True))
    op.create_foreign_key('order_shipping_address_id_fkey', 'order', 'address', ['shipping_address_id'], ['id'], ondelete='SET NULL')
    op.create_foreign_key('order_billing_address_id_fkey', 'order', 'address', ['billing_address_id'], ['id'], ondelete='SET NULL')
    op.drop_table('orderaddresslink')
    # ### end Alembic commands ###
