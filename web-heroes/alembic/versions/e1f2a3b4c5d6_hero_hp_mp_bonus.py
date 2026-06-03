"""add hp_bonus and mp_bonus to heroes

Revision ID: e1f2a3b4c5d6
Revises: d0e1f2a3b4c5
Create Date: 2026-06-03 14:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision: str = 'e1f2a3b4c5d6'
down_revision: Union[str, Sequence[str], None] = 'd0e1f2a3b4c5'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    hero_columns = [col["name"] for col in inspect(conn).get_columns("heroes")]

    if "hp_bonus" not in hero_columns:
        op.add_column("heroes", sa.Column("hp_bonus", sa.Integer(), nullable=False, server_default="0"))

    if "mp_bonus" not in hero_columns:
        op.add_column("heroes", sa.Column("mp_bonus", sa.Integer(), nullable=False, server_default="0"))


def downgrade() -> None:
    conn = op.get_bind()
    hero_columns = [col["name"] for col in inspect(conn).get_columns("heroes")]

    if "hp_bonus" in hero_columns:
        op.drop_column("heroes", "hp_bonus")

    if "mp_bonus" in hero_columns:
        op.drop_column("heroes", "mp_bonus")
