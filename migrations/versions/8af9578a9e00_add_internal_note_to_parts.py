"""Add internal_note to parts

Revision ID: 8af9578a9e00
Revises: c5f7fe66fb1d
Create Date: 2025-04-13 14:56:38.983179

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '8af9578a9e00'
down_revision: Union[str, None] = 'c5f7fe66fb1d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('parts', sa.Column('internal_note', sa.Text(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('parts', 'internal_note')
    # ### end Alembic commands ###
