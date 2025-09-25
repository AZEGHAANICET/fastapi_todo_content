"""Create phone number for user column

Revision ID: 247215ee42e0
Revises: 
Create Date: 2025-09-25 00:12:20.753956

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '247215ee42e0'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column("users", sa.Column("phone_number", sa.String, nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    pass
