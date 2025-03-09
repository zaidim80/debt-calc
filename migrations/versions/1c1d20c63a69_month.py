"""month

Revision ID: 1c1d20c63a69
Revises: ec4b1abad651
Create Date: 2025-03-08 21:21:20.623747

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1c1d20c63a69'
down_revision: Union[str, None] = 'ec4b1abad651'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('payment', sa.Column('month', sa.String(length=12), nullable=True))
    
    # Update existing records to set month based on date
    op.execute("UPDATE payment SET month = to_char(date, 'YYYY-MM')")
    
    op.alter_column('payment', 'month', nullable=False)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('payment', 'month')
    # ### end Alembic commands ###
