"""add hotel status field

Revision ID: 002_add_status
Revises: 001_initial
Create Date: 2025-02-07 00:00:01

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '002_add_status'
down_revision = '001_initial'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Add status column to hotels table
    op.add_column('hotels', sa.Column('status', sa.String(), nullable=True))
    
    # Set default value for existing rows
    op.execute("UPDATE hotels SET status = 'active' WHERE status IS NULL")


def downgrade() -> None:
    op.drop_column('hotels', 'status')