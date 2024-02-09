"""init

Revision ID: 249cb8918574
Revises: 
Create Date: 2024-02-09 22:37:41.591012

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '249cb8918574'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('debt',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=100), nullable=False),
    sa.Column('date', sa.Date(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('period', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('user',
    sa.Column('email', sa.String(length=200), nullable=False),
    sa.Column('name', sa.String(length=200), nullable=False),
    sa.Column('admin', sa.Boolean(), server_default=sa.text('false'), nullable=False),
    sa.PrimaryKeyConstraint('email')
    )
    op.create_table('payment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('debt_id', sa.Integer(), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('author_email', sa.String(length=200), nullable=False),
    sa.ForeignKeyConstraint(['author_email'], ['user.email'], ),
    sa.ForeignKeyConstraint(['debt_id'], ['debt.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('payment')
    op.drop_table('user')
    op.drop_table('debt')
    # ### end Alembic commands ###
