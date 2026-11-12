
"""Add Category and Product relationship

Revision ID: 67e19ce73d41
Revises: 4233e40d7f0e
"""

from alembic import op
import sqlalchemy as sa


revision = '67e19ce73d41'
down_revision = '4233e40d7f0e'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'categories',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=100), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.add_column(
            sa.Column('category_id', sa.Integer(), nullable=False)
        )
        batch_op.create_foreign_key(
            'fk_products_category_id_categories',
            'categories',
            ['category_id'],
            ['id']
        )


def downgrade():
    with op.batch_alter_table('products', schema=None) as batch_op:
        batch_op.drop_constraint(
            'fk_products_category_id_categories',
            type_='foreignkey'
        )
        batch_op.drop_column('category_id')

    op.drop_table('categories')
