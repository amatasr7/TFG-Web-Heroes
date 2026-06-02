"""merge heads

Revision ID: 7f2d9b4a6c1e
Revises: e938c6191d81, 4b9521c5d957
Create Date: 2026-06-02 00:10:00.000000
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '7f2d9b4a6c1e'
down_revision: Union[str, Sequence[str], None] = ('e938c6191d81', '4b9521c5d957')
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
