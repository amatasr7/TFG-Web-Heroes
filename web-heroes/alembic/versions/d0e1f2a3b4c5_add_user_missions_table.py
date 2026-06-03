"""add user_missions table

Revision ID: d0e1f2a3b4c5
Revises: c9d0e1f2a3b4
Create Date: 2026-06-03 13:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision: str = 'd0e1f2a3b4c5'
down_revision: Union[str, Sequence[str], None] = 'c9d0e1f2a3b4'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    conn = op.get_bind()
    existing_tables = inspect(conn).get_table_names()
    if "user_missions" not in existing_tables:
        op.create_table(
            "user_missions",
            sa.Column("id", sa.Integer(), nullable=False),
            sa.Column("user_id", sa.Integer(), nullable=False),
            sa.Column("mission_id", sa.Integer(), nullable=False),
            sa.Column("completed_at", sa.DateTime(), nullable=False),
            sa.ForeignKeyConstraint(["user_id"], ["users.id"], ondelete="CASCADE"),
            sa.ForeignKeyConstraint(["mission_id"], ["missions.id"], ondelete="CASCADE"),
            sa.PrimaryKeyConstraint("id"),
            sa.UniqueConstraint("user_id", "mission_id"),
        )
        op.create_index(op.f("ix_user_missions_id"), "user_missions", ["id"], unique=False)


def downgrade() -> None:
    conn = op.get_bind()
    existing_tables = inspect(conn).get_table_names()
    if "user_missions" in existing_tables:
        op.drop_index(op.f("ix_user_missions_id"), table_name="user_missions")
        op.drop_table("user_missions")
