"""add foreign_key to posts table

Revision ID: 13df52042c71
Revises: a6d87dfe07ca
Create Date: 2021-12-30 11:46:47.797851

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '13df52042c71'
down_revision = 'a6d87dfe07ca'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column(
        'posts',
        sa.Column('owner_id', sa.Integer(), nullable=False),
    )
    op.create_foreign_key(
        'posts_users_fk',
        source_table="posts",
        referent_table="users",
        local_cols=['owner_id'],
        remote_cols=['id'],
        ondelete="CASCADE"
    )
    pass


def downgrade():
    op.drop_constraint('posts_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
