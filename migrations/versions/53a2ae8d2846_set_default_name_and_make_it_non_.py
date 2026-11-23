"""set default name and make it non-nullable

Revision ID: 53a2ae8d2846
Revises: b162fd13812a
Create Date: 2026-11-23 10:07:39.346554

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import pgvector.sqlalchemy


# revision identifiers, used by Alembic.
revision: str = '53a2ae8d2846'
down_revision: Union[str, Sequence[str], None] = 'b162fd13812a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.execute("UPDATE product SET name = 'без назви' WHERE name IS NULL")
    
    op.alter_column(
        'product', 
        'name',
        existing_type=sa.VARCHAR(length=150),
        nullable=False
    )


def downgrade() -> None:
    op.alter_column(
        'product', 
        'name',
        existing_type=sa.VARCHAR(length=150),
        nullable=True
    )
