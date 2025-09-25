"""Create phone number for user column

Revision ID: 345202bbbc44
Revises: 247215ee42e0
Create Date: 2025-09-25 00:17:23.149088

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '345202bbbc44'
down_revision: Union[str, Sequence[str], None] = '247215ee42e0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
