"""add_rejection_reason_to_adoption_requests

Revision ID: 0ebe3e3d8dfa
Revises: b2c41e048809
Create Date: 2025-11-26 22:40:27.636397

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0ebe3e3d8dfa'
down_revision: Union[str, Sequence[str], None] = 'b2c41e048809'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('adoption_requests', sa.Column(
        'rejection_reason', sa.Text(), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('adoption_requests', 'rejection_reason')
