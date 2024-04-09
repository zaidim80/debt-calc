from sqlalchemy.ext.asyncio import AsyncConnection
import sqlalchemy as sa
import logging
import pydantic as pd

import schemas as s
import models as m


log = logging.getLogger()


class PaymentActions:
    @staticmethod
    async def get_one(dbc: AsyncConnection, user: s.User, item_id: int):
        res = await dbc.execute(
            sa.select(
                m.payment.c.id,
                m.payment.c.date,
                m.payment.c.amount,
                m.payment.c.author_id,
                m.user.c.email.label("author_email"),
                m.user.c.name.label("author_name"),
            )
            .select_from(m.payment, m.user)
            .where(
                m.user.c.email == m.payment.c.author_email,
                m.payment.c.id == item_id,
            )
        )
        item = res.first()
        result = s.Payment.model_validate(item, from_attributes=True)
        result.author = s.UserOut(
            email=item.author_email,
            name=item.author_name,
        )
        return result

    @staticmethod
    async def get_list(dbc: AsyncConnection, user: s.User, debt_id: int | None = None):
        query = (
            sa.select(
                m.payment.c.id,
                m.payment.c.date,
                m.payment.c.amount,
                m.payment.c.author_id,
                m.user.c.email.label("author_email"),
                m.user.c.name.label("author_name"),
            )
            .select_from(m.payment)
            .order_by(m.payment.c.date)
        )
        if debt_id:
            query = query.where(
                m.user.c.email == m.payment.c.author_email,
                m.payment.c.debt_id == debt_id,
            )
        else:
            query = query.where(m.user.c.email == m.payment.c.author_email)
        res = await dbc.execute(query)
        items = res.fetchall()
        return [(
            s.Payment
            .model_validate(item, from_attributes=True)
            .setattr("author", s.UserOut(name=item.author_name, email=item.author_email))
        ) for item in items]

    @staticmethod
    async def create(dbc: AsyncConnection, user: s.User, data: s.PaymentData):
        res = await dbc.execute(
            sa.select(
                m.debt.c.id, m.debt.c.amount, m.debt.c.date, m.debt.c.name, m.debt.c.period, m.debt.c.rate,
                m.debt.c.author_email, m.user.c.name.label("author_name"),
            )
            .select_from(m.debt, m.user)
            .where(
                m.debt.c.author_email == m.user.c.email,
                m.debt.c.id == data.debt_id,
            )
        )
        debt = res.first()
        if debt is None:
            raise pd.ValidationError(
                []
            )
        else:
            res = await dbc.execute(
                sa.insert(m.payment)
                .values(date=data.date, amount=data.amount, author_id=user.id, debt_id=data.debt_id, )
                .returning(m.payment.c.id, m.payment.c.date, m.payment.c.amount, )
            )
            item = res.first()
            result = s.Payment.model_validate(item, from_attributes=True)
            result.author = user
            result.debt = None
            return result


actions = PaymentActions()
