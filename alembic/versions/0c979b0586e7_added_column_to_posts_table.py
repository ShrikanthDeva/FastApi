"""added column to  posts table

Revision ID: 0c979b0586e7
Revises: 72f30611aa48
Create Date: 2022-01-14 17:54:44.234023

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0c979b0586e7'
down_revision = '72f30611aa48'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('pots','content')
    pass
