"""add shop tables and user gold

Revision ID: b3c4d5e6f7a8
Revises: 7f2d9b4a6c1e
Create Date: 2026-06-02 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b3c4d5e6f7a8'
down_revision: Union[str, Sequence[str], None] = '7f2d9b4a6c1e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add gold column to users table
    op.add_column('users', sa.Column('gold', sa.Integer(), nullable=False, server_default='50'))

    # Create shop_items table (vendor inventory)
    op.create_table(
        'shop_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('item_id', sa.Integer(), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['item_id'], ['items.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('item_id'),
    )
    op.create_index(op.f('ix_shop_items_id'), 'shop_items', ['id'], unique=False)

    # Create user_items table (player inventory)
    op.create_table(
        'user_items',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('item_id', sa.Integer(), nullable=False),
        sa.Column('quantity', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['item_id'], ['items.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'item_id'),
    )
    op.create_index(op.f('ix_user_items_id'), 'user_items', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_user_items_id'), table_name='user_items')
    op.drop_table('user_items')
    op.drop_index(op.f('ix_shop_items_id'), table_name='shop_items')
    op.drop_table('shop_items')
    op.drop_column('users', 'gold')
