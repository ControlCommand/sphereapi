"""add the rest of columns to posts table

Revision ID: 2dddda8d080d
Revises: 48d5af040e00
Create Date: 2023-09-03 01:00:20.565741

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2dddda8d080d'
down_revision: Union[str, None] = '48d5af040e00'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('posts', sa.Column('published', sa.Boolean(), nullable=False, server_default='TRUE'))
    op.add_column('posts', sa.Column('created_at', 
                                     sa.TIMESTAMP(timezone=True), 
                                     nullable=False, 
                                     server_default=sa.text('NOW()')))
    
    pass


def downgrade():
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
