"""add is_active field to debt

Revision ID: add_is_active_debt
Revises: 1c1d20c63a69
Create Date: 2026-02-04 12:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'add_is_active_debt'
down_revision: Union[str, None] = '1c1d20c63a69'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Добавляем колонку is_active как nullable
    op.add_column('debt', sa.Column('is_active', sa.Boolean(), nullable=True))
    
    # Заполняем существующие записи значением True
    op.execute("UPDATE debt SET is_active = true")
    
    # Теперь делаем колонку NOT NULL с дефолтным значением
    op.alter_column('debt', 'is_active', nullable=False, server_default='true')


def downgrade() -> None:
    # Удаляем колонку is_active
    op.drop_column('debt', 'is_active')
