"""create posts table

Revision ID: 8bf10288be34
Revises: 
Create Date: 2025-02-17 12:44:36.708596

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
# from sqlalchemy.sql.expression import func


# revision identifiers, used by Alembic.
revision: str = '8bf10288be34'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.create_table(
        "posts",
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True), 
        sa.Column('title',sa.String(), nullable=False),
        sa.Column('content',sa.String(), nullable=False),
        sa.Column('published', sa.Boolean(),server_default=sa.text('true'), nullable=False),
        sa.Column('created_at', sa.TIMESTAMP(),nullable=False,server_default=sa.func.now()),
        )
    pass


def downgrade():
    op.drop_table('posts')
    pass
