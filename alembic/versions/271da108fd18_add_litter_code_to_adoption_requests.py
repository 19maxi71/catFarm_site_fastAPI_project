"""add_litter_code_to_adoption_requests

Revision ID: 271da108fd18
Revises: 45d38780c4ab
Create Date: 2025-11-06 22:19:12.192783

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '271da108fd18'
down_revision: Union[str, Sequence[str], None] = '45d38780c4ab'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.add_column('adoption_requests', sa.Column('litter_code', sa.String(length=20), nullable=True))


def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('adoption_requests', 'litter_code')
