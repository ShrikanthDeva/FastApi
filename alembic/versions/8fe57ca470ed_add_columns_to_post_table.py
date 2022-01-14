"""add columns to post table

Revision ID: 8fe57ca470ed
Revises: 642b4aebd1b1
Create Date: 2022-01-14 18:15:29.878238

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '8fe57ca470ed'
down_revision = '642b4aebd1b1'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column('created_at', sa.TIMESTAMP(timezone=True),server_default=sa.text('now()') ,nullable=False),)

    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts','created_at')
    pass
