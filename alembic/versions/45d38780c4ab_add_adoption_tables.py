"""add adoption tables

Revision ID: 45d38780c4ab
Revises: 3da59699d7a0
Create Date: 2025-11-05 23:52:33.311731

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '45d38780c4ab'
down_revision: Union[str, Sequence[str], None] = '3da59699d7a0'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Add adoption tables
    op.create_table('adoption_questions',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('question_text', sa.String(length=500), nullable=False),
        sa.Column('question_type', sa.String(length=50), nullable=False),
        sa.Column('options', sa.Text(), nullable=True),
        sa.Column('is_required', sa.Boolean(), nullable=True),
        sa.Column('order', sa.Integer(), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('adoption_requests',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('customer_email', sa.String(length=255), nullable=False),
        sa.Column('customer_name', sa.String(length=255), nullable=False),
        sa.Column('phone', sa.String(length=50), nullable=True),
        sa.Column('custom_answers', sa.Text(), nullable=True),
        sa.Column('terms_agreed', sa.Boolean(), nullable=True),
        sa.Column('subscription', sa.Boolean(), nullable=True),
        sa.Column('submitted_at', sa.DateTime(timezone=True), server_default=sa.text('(CURRENT_TIMESTAMP)'), nullable=True),
        sa.Column('status', sa.String(length=50), nullable=True),
        sa.Column('notification_sent_at', sa.DateTime(timezone=True), nullable=True),
        sa.PrimaryKeyConstraint('id')
    )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop adoption tables
    op.drop_table('adoption_requests')
    op.drop_table('adoption_questions')
