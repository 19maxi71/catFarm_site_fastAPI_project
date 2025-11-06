"""rename_order_to_display_order_in_adoption_questions

Revision ID: b2c41e048809
Revises: 271da108fd18
Create Date: 2025-11-06 23:06:40.997502

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'b2c41e048809'
down_revision: Union[str, Sequence[str], None] = '271da108fd18'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Rename 'order' column to 'display_order' in adoption_questions table
    op.alter_column('adoption_questions', 'order', new_column_name='display_order')


def downgrade() -> None:
    """Downgrade schema."""
    # Rename 'display_order' column back to 'order' in adoption_questions table
    op.alter_column('adoption_questions', 'display_order', new_column_name='order')
