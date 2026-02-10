"""Initial migration for todos table

Revision ID: 001_initial_todos
Revises: 
Create Date: 2026-02-08 00:00:00.000000

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects.postgresql import ENUM


# revision identifiers
revision = '001_initial_todos'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    # Create the priority enum type
    priority_enum = ENUM('low', 'medium', 'high', name='priority', create_type=False)
    priority_enum.create(op.get_bind(), checkfirst=True)
    
    # Create the todos table
    op.create_table(
        'todos',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(length=140), nullable=False),
        sa.Column('notes', sa.String(length=500), nullable=True),
        sa.Column('priority', priority_enum, server_default='medium', nullable=False),
        sa.Column('completed', sa.Boolean(), server_default=sa.text('false'), nullable=False),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('updated_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=False),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id', name=op.f('pk_todos'))
    )


def downgrade() -> None:
    # Drop the todos table
    op.drop_table('todos')
    
    # Drop the priority enum type
    ENUM(name='priority').drop(op.get_bind(), checkfirst=True)