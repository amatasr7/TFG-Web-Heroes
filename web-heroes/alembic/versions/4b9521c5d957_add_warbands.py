"""add warband tables

Revision ID: 4b9521c5d957
Revises: e96c734a9046
Create Date: 2026-06-02 00:00:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '4b9521c5d957'
down_revision: Union[str, Sequence[str], None] = 'e96c734a9046'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.create_table(
        'warbands',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id')
    )
    op.create_index(op.f('ix_warbands_id'), 'warbands', ['id'], unique=False)

    op.create_table(
        'warband_heroes',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('warband_id', sa.Integer(), nullable=False),
        sa.Column('hero_id', sa.Integer(), nullable=False),
        sa.Column('slot', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['hero_id'], ['heroes.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['warband_id'], ['warbands.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('warband_id', 'slot'),
        sa.UniqueConstraint('warband_id', 'hero_id')
    )
    op.create_index(op.f('ix_warband_heroes_id'), 'warband_heroes', ['id'], unique=False)


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_index(op.f('ix_warband_heroes_id'), table_name='warband_heroes')
    op.drop_table('warband_heroes')
    op.drop_index(op.f('ix_warbands_id'), table_name='warbands')
    op.drop_table('warbands')
