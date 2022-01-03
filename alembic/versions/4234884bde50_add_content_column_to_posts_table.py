"""add content column to posts table

Revision ID: 4234884bde50
Revises: bfd2c9372b69
Create Date: 2021-12-30 11:31:08.337483

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4234884bde50'
down_revision = 'bfd2c9372b69'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'posts',
        sa.Column('content', sa.String(), nullable=False)
    )
    pass


def downgrade():
    op.drop_column("posts", "content")
    pass
