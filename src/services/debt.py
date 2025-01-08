from sqlalchemy.ext.asyncio import AsyncConnection
import sqlalchemy as sa
from fastapi.security import OAuth2PasswordBearer
import logging
from datetime import datetime
import math

import schemas as s
import models as m


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
log = logging.getLogger()


class DebtActions:
    @staticmethod
    def calc_payment(rate: float, period: int, debt: float) -> int:
        return round(debt * (rate + rate / (pow(1 + rate, period) - 1)))

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
        result.default_payment = self.calc_payment(mrate, result.period, result.amount)
        month = result.date.month - 1
        year = result.date.year
        loan_payed = 0
        loan_debt = result.amount
        now = datetime.now()
        today = f"{now.year}-{now.month:02d}"
        month_new_payment = result.default_payment
        schedule = []
        for i in range(1, result.period + 1):
            month += 1
            current_month = month % 12 + 1
            current_year = year + math.floor(month / 12)
            month_id = f"{current_year:04d}-{current_month:02d}"
            # month_title = f"{current_month:02d}.{current_year:04d}"
            # month_title_short = f"{current_month:02d}.{(current_year % 100):02d}"
            month_payed = month_id in payments
            loan_debt *= 1 + mrate
            month_tax = loan_debt * mrate

            if month_payed:
                month_payment = payments[month_id].amount
                loan_payed += month_payment
                loan_debt -= month_payment
                month_new_payment = self.calc_payment(mrate, result.period - i, loan_debt)
                rec_payment = result.default_payment
                payed_summ = month_payment
            elif today > month_id:
                month_payment = 0
                month_new_payment = self.calc_payment(mrate, result.period - i, loan_debt)
                rec_payment = month_new_payment
                payed_summ = 0
            else:
                month_payment = month_new_payment
                loan_debt -= month_payment
                rec_payment = month_payment
                payed_summ = 0
            fp = s.FuturePayment(
                id=i,
                default=rec_payment,
                amount=payed_summ,
                interest=round(month_tax),
                redemption=round(month_payment - month_tax),
                total=round(loan_payed),
                remainder=round(loan_debt),
                date=month_id,
            )
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
