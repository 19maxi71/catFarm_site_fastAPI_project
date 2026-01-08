"""add privacy_consent to adoption_requests

Revision ID: f85b74276a0a
Revises: 0ebe3e3d8dfa
Create Date: 2026-01-08 23:30:00.000000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'f85b74276a0a'
down_revision = '0ebe3e3d8dfa'
branch_labels = None
depends_on = None


def upgrade():
    # Add privacy_consent column to adoption_requests table
    op.add_column('adoption_requests', sa.Column('privacy_consent', sa.Boolean(), nullable=True))

    # Set default value for existing rows
    op.execute('UPDATE adoption_requests SET privacy_consent = false WHERE privacy_consent IS NULL')

    # Make it non-nullable after setting defaults
    op.alter_column('adoption_requests', 'privacy_consent', nullable=False, server_default=sa.false())


def downgrade():
    # Remove privacy_consent column
    op.drop_column('adoption_requests', 'privacy_consent')
