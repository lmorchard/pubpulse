"""empty message

Revision ID: 6726f6c6fece
Revises: 6c5b9a0941c8
Create Date: 2024-04-25 01:16:11.902536

"""
from alembic import op
import sqlalchemy as sa
import pgvector

# revision identifiers, used by Alembic.
revision = '6726f6c6fece'
down_revision = '6c5b9a0941c8'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('status_embeddings',
    sa.Column('url', sa.String(), nullable=False),
    sa.Column('embedding', pgvector.sqlalchemy.Vector(dim=384), nullable=True),
    sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False),
    sa.PrimaryKeyConstraint('url')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('status_embeddings')
    # ### end Alembic commands ###
