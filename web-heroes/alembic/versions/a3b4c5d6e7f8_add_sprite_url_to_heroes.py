"""add sprite_url to heroes

Revision ID: a3b4c5d6e7f8
Revises: f2g3h4i5j6k7
Create Date: 2026-06-05 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


revision: str = 'a3b4c5d6e7f8'
down_revision: Union[str, Sequence[str], None] = 'f2g3h4i5j6k7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    hero_columns = [col["name"] for col in inspect(conn).get_columns("heroes")]

    if "sprite_url" not in hero_columns:
        op.add_column("heroes", sa.Column("sprite_url", sa.String(255), nullable=True))


def downgrade() -> None:
    conn = op.get_bind()
    hero_columns = [col["name"] for col in inspect(conn).get_columns("heroes")]

    if "sprite_url" in hero_columns:
        op.drop_column("heroes", "sprite_url")
