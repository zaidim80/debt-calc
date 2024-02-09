import sqlalchemy as sa


metadata = sa.MetaData()


user= sa.Table(
    'user',
    metadata,
    sa.Column('email', sa.String(200), primary_key=True),
    sa.Column('name', sa.String(200), nullable=False),
    sa.Column('admin', sa.Boolean, nullable=False, server_default=sa.false()),
)


debt= sa.Table(
    'debt',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('name', sa.String(100), nullable=False),
    sa.Column('date', sa.Date, nullable=False),
    sa.Column('amount', sa.Integer, nullable=False),
    sa.Column('period', sa.Integer, nullable=False),
)


payment= sa.Table(
    'payment',
    metadata,
    sa.Column('id', sa.Integer, primary_key=True),
    sa.Column('debt_id', sa.Integer, sa.ForeignKey('debt.id'), nullable=False),
    sa.Column('date', sa.DateTime, nullable=False),
    sa.Column('amount', sa.Integer, nullable=False),
    sa.Column('author_email', sa.String(200), sa.ForeignKey('user.email'), nullable=False),
)
