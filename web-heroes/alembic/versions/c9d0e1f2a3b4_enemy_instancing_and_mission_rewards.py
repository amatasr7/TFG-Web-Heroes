"""enemy instancing and mission item rewards

Revision ID: c9d0e1f2a3b4
Revises: b3c4d5e6f7a8
Create Date: 2026-06-03 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy import inspect


# revision identifiers, used by Alembic.
revision: str = 'c9d0e1f2a3b4'
down_revision: Union[str, Sequence[str], None] = 'b3c4d5e6f7a8'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Drop hp_current from enemies — Enemy is now a pure template.
    # Only drop if the column actually exists (handles fresh DBs where
    # the column was never created by an earlier migration).
    conn = op.get_bind()
    enemy_columns = [col["name"] for col in inspect(conn).get_columns("enemies")]
    if "hp_current" in enemy_columns:
        with op.batch_alter_table("enemies") as batch_op:
            batch_op.drop_column("hp_current")

    # Add item_reward_ids to missions (JSON list of item IDs awarded on completion).
    # MySQL does not allow DEFAULT on JSON columns, so: add nullable → backfill → NOT NULL.
    mission_columns = [col["name"] for col in inspect(conn).get_columns("missions")]
    if "item_reward_ids" not in mission_columns:
        op.add_column("missions", sa.Column("item_reward_ids", sa.JSON(), nullable=True))
        op.execute("UPDATE missions SET item_reward_ids = '[]' WHERE item_reward_ids IS NULL")
        with op.batch_alter_table("missions") as batch_op:
            batch_op.alter_column("item_reward_ids", existing_type=sa.JSON(), nullable=False)


def downgrade() -> None:
    conn = op.get_bind()

    mission_cols = [col["name"] for col in inspect(conn).get_columns("missions")]
    if "item_reward_ids" in mission_cols:
        op.drop_column("missions", "item_reward_ids")

    enemy_columns = [col["name"] for col in inspect(conn).get_columns("enemies")]
    if "hp_current" not in enemy_columns:
        with op.batch_alter_table("enemies") as batch_op:
            batch_op.add_column(
                sa.Column("hp_current", sa.Integer(), nullable=False, server_default="10")
            )
