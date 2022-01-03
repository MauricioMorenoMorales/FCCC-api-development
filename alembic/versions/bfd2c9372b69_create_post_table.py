"""create post table

Revision ID: bfd2c9372b69
Revises:
Create Date: 2021-12-22 11:46:49.870607

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'bfd2c9372b69'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
	op.create_table(
		'posts',
		sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
		sa.Column('title', sa.String(), nullable=False)
	)
	pass


def downgrade():
	op.drop_table('posts')
	pass
