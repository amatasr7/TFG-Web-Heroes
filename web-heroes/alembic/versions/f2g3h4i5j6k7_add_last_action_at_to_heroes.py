"""add last_action_at to heroes

Revision ID: f2g3h4i5j6k7
Revises: e1f2a3b4c5d6
Create Date: 2026-06-03 16:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


revision: str = 'f2g3h4i5j6k7'
down_revision: Union[str, Sequence[str], None] = 'e1f2a3b4c5d6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    hero_columns = [col["name"] for col in inspect(conn).get_columns("heroes")]

    if "last_action_at" not in hero_columns:
        op.add_column("heroes", sa.Column("last_action_at", sa.DateTime(), nullable=True))


def downgrade() -> None:
    conn = op.get_bind()
    hero_columns = [col["name"] for col in inspect(conn).get_columns("heroes")]

    if "last_action_at" in hero_columns:
        op.drop_column("heroes", "last_action_at")
