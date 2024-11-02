from sqlalchemy.ext.asyncio import AsyncConnection
import sqlalchemy as sa
from fastapi.security import OAuth2PasswordBearer
import logging
from datetime import datetime

import schemas as s
import models as m


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
log = logging.getLogger()


class DebtActions:
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
        result.payments = []
        payments = {}
        for item in res.fetchall():
            result.payments.append(s.Payment.model_validate(
                item,
                from_attributes=True,
                context={"author": s.UserOut(name=item.author_name, email=item.author_email)},
            ))
            pid = f"{item.date.year}-{item.date.month:02d}"
            payments[pid] = item
        mrate = result.rate / 12 / 100
        result.default_payment = round(result.amount * (mrate + mrate / (pow(1 + mrate, result.period) - 1)))
        month = result.date.month - 1
        year = result.date.year
        payed = 0
        debt = result.amount
        now = datetime.now()
        today = f"{now.year}-{now.month:02d}"
        schedule = []
        for i in range(1, result.period + 1):
            month += 1
            cur_month = month % 12
            cur_year = year + (month // 12)
            pid = f"{cur_year}-{cur_month:02d}"
            new_payment = (
                round(debt * (mrate + mrate / (pow(1 + mrate, result.period - i) - 1))) if result.period - i
                else debt
            )
            if pid in payments:
                # оплата за данный месяц уже внесена
                payed += payments[pid].amount
                amount = payments[pid].amount
                debt -= amount
            elif today > pid:
                # просрочка
                amount = 0
            else:
                # будущее
                pass
            fp = {
                "id": i,
                "amount": new_payment,
                "interest": 0,
                "redemption": 0,
                "total": payed,
                "remainder": debt,
                "date": pid,
            }
            schedule.append(fp)
        result.schedule = schedule

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
