"""add content column to posts table

Revision ID: ad3923569fb4
Revises: 5911d873a89e
Create Date: 2023-09-03 00:18:51.044904

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ad3923569fb4'
down_revision: Union[str, None] = '5911d873a89e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts',
                  sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade():
    op.drop_column('posts', 'content')
    pass
