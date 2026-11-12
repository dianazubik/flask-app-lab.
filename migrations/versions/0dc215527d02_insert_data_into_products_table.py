
"""Insert data into products table

Revision ID: 0dc215527d02
Revises: ca47e4bd2c8c
Create Date: 2026-11-12 19:30:23.827587

"""
from alembic import op
import sqlalchemy as sa


revision = '0dc215527d02'
down_revision = 'ca47e4bd2c8c'
branch_labels = None
depends_on = None


def upgrade():
    categories_table = sa.table(
        'categories',
        sa.column('id', sa.Integer),
        sa.column('name', sa.String)
    )

    products_table = sa.table(
        'products',
        sa.column('name', sa.String),
        sa.column('price', sa.Float),
        sa.column('category_id', sa.Integer),
        sa.column('active', sa.Boolean)
    )

    # Додаємо нові категорії
    op.bulk_insert(
        categories_table,
        [
            {'id': 3, 'name': 'Books'},
            {'id': 4, 'name': 'Clothing'}
        ]
    )

    # Додаємо нові товари
    op.bulk_insert(
        products_table,
        [
            {
                'name': 'Laptop',
                'price': 1200.0,
                'active': True,
                'category_id': 3
            },
            {
                'name': 'Smartphone',
                'price': 800.0,
                'active': True,
                'category_id': 3
            },
            {
                'name': 'Novel',
                'price': 15.0,
                'active': False,
                'category_id': 4
            },
            {
                'name': 'T-Shirt',
                'price': 25.0,
                'active': True,
                'category_id': 4
            }
        ]
    )


def downgrade():
    # Видаляємо додані товари
    op.execute(
        sa.text("""
            DELETE FROM products
            WHERE name IN ('Laptop', 'Smartphone', 'Novel', 'T-Shirt')
        """)
    )

    # Видаляємо додані категорії
    op.execute(
        sa.text("""
            DELETE FROM categories
            WHERE id IN (3, 4)
        """)
    )
