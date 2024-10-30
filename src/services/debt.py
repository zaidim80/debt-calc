from sqlalchemy.ext.asyncio import AsyncConnection
import sqlalchemy as sa
from fastapi.security import OAuth2PasswordBearer
import logging

import schemas as s
import models as m


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
log = logging.getLogger()


class DebtActions:
    @staticmethod
    def get_month_payment(rate, months, sum):
        mrate = rate / 12 / 100
        return sum * (mrate + mrate / (pow(1 + mrate, months) - 1))

    async def get_one(self, dbc: AsyncConnection, user: s.User, item_id: int):
        res = await dbc.execute(
            sa.select(
                m.debt.c.id,
                m.debt.c.name,
                m.debt.c.date,
                m.debt.c.amount,
                m.debt.c.period,
                m.debt.c.rate,
                m.user.c.email.label("author_email"),
                m.user.c.name.label("author_name"),
            )
            .select_from(m.debt, m.user)
            .where(
                m.user.c.email == m.debt.c.author_email,
                m.debt.c.id == item_id,
            )
        )
        item = res.first()
        result = s.DebtInfo.model_validate(
            item,
            from_attributes=True,
            context={"author": s.UserOut(name=item.author_name, email=item.author_email)},
        )
        res = await dbc.execute(
            sa.select(
                m.payment.c.id,
                m.payment.c.amount,
                m.payment.c.date,
                m.user.c.email.label("author_email"),
                m.user.c.name.label("author_name"),
            )
            .select_from(m.payment, m.user)
            .where(
                m.user.c.email == m.payment.c.author_email,
                m.payment.c.debt_id == result.id,
            )
        )
        result.payments = [s.Payment.model_validate(
            item,
            from_attributes=True,
            context={"author": s.UserOut(name=item.author_name, email=item.author_email)},
        ) for item in res.fetchall()]
        result.default_payment = round(self.get_month_payment(
            result.rate,
            result.period,
            result.amount,
        ), 2)
        return result

    @staticmethod
    async def get_list(dbc: AsyncConnection, user: s.User):
        query = (
            sa.select(
                m.debt.c.id,
                m.debt.c.name,
                m.debt.c.date,
                m.debt.c.amount,
                m.debt.c.period,
                m.debt.c.rate,
                m.user.c.email.label("author_email"),
                m.user.c.name.label("author_name"),
            )
            .select_from(m.debt)
            .order_by(m.debt.c.date)
        )
        query = query.where(m.user.c.email == m.debt.c.author_email)
        res = await dbc.execute(query)
        return [s.Debt.model_validate(
            item,
            from_attributes=True,
            context={"author": s.UserOut(name=item.author_name, email=item.author_email)},
        ) for item in res.fetchall()]


actions = DebtActions()
