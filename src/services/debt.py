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
    def _calc_payment(rate: float, period: int, debt: float) -> int:
        return round(debt * (rate + rate / (pow(1 + rate, period) - 1)))
    
    @staticmethod
    async def _fetch_debt(dbc: AsyncConnection, user: s.User, debt_id: int):
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
                m.debt.c.id == debt_id,
            )
        )
        item = res.first()
        return s.DebtInfo.model_validate(
            item,
            from_attributes=True,
            context={"author": s.UserOut(name=item.author_name, email=item.author_email)},
        )
    
    @staticmethod
    async def _fetch_debt_payments(dbc: AsyncConnection, user: s.User, debt_id: int):
        res = await dbc.execute(
            sa.select(
                m.payment.c.id,
                m.payment.c.amount,
                m.payment.c.date,
                m.payment.c.month,
                m.user.c.email.label("author_email"),
                m.user.c.name.label("author_name"),
            )
            .select_from(m.payment, m.user)
            .where(
                m.user.c.email == m.payment.c.author_email,
                m.payment.c.debt_id == debt_id,
            )
        )
        return [s.Payment.model_validate(
            item,
            from_attributes=True,
            context={"author": s.UserOut(name=item.author_name, email=item.author_email)},
        ) for item in res.fetchall()]

    @staticmethod
    async def _update_or_create_payment(dbc: AsyncConnection, user: s.User, payment: s.PaymentUpdate):
        res = await dbc.execute(
            sa.select(m.payment.c.id)
            .where(
                m.payment.c.debt_id == payment.debt_id,
                m.payment.c.month == payment.month,
            )
        )
        payment_id = res.scalar()
        if payment_id:
            await dbc.execute(
                sa.update(m.payment)
                .where(m.payment.c.id == payment_id)
                .values(amount=payment.amount)
                .returning(m.payment.c.id)
            )
        else:
            res = await dbc.execute(
                sa.insert(m.payment)
                .values(
                    debt_id=payment.debt_id,
                    amount=payment.amount,
                    date=datetime.now(),
                    month=payment.month,
                    author_email=user.email,
                )
                .returning(m.payment.c.id)
            )
            payment_id = res.scalar()
        return payment_id

    @staticmethod
    async def _fetch_payment(dbc: AsyncConnection, user: s.User, payment_id: int):
        res = await dbc.execute(
            sa.select(
                m.payment.c.id,
                m.payment.c.amount,
                m.payment.c.date,
                m.payment.c.month,
                m.user.c.email.label("author_email"),
                m.user.c.name.label("author_name"),
            )
            .select_from(m.payment, m.user)
            .where(
                m.payment.c.id == payment_id,
                m.user.c.email == m.payment.c.author_email,
            )
        )
        item = res.first()
        return s.Payment(
            id=item.id,
            amount=item.amount,
            date=item.date,
            month=item.month,
            author=s.UserOut(name=item.author_name, email=item.author_email),
        )

    @staticmethod
    async def _fetch_debts(dbc: AsyncConnection, user: s.User):
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

    async def get_one(self, dbc: AsyncConnection, user: s.User, item_id: int):
        result = await self._fetch_debt(dbc, user, item_id)
        payments_data = await self._fetch_debt_payments(dbc, user, item_id)
        result.payments = []
        payments = {}
        for item in payments_data:
            result.payments.append(item)
            pid = item.month
            payments[pid] = item
        mrate = result.rate / 12 / 100
        result.default_payment = self._calc_payment(mrate, result.period, result.amount)
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
            month_payed = month_id in payments
            loan_debt *= 1 + mrate
            month_tax = loan_debt * mrate

            if month_payed:
                month_payment = payments[month_id].amount
                loan_payed += month_payment
                loan_debt -= month_payment
                month_new_payment = self._calc_payment(mrate, result.period - i, loan_debt)
                rec_payment = result.default_payment
                payed_summ = month_payment
            elif today > month_id:
                month_payment = 0
                month_new_payment = self._calc_payment(mrate, result.period - i, loan_debt)
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

    async def get_list(self, dbc: AsyncConnection, user: s.User):
        return await self._fetch_debts(dbc, user)

    async def process_payment(
        self,
        dbc: AsyncConnection,
        user: s.User,
        debt_id: int,
        payment: s.PaymentPay,
    ) -> s.Payment:
        # проверяем, что займ существует
        await self._fetch_debt(dbc, user, debt_id)
        # обновляем существующй или создаем новый платеж
        payment_id = await self._update_or_create_payment(dbc, user, payment)
        # получаем платеж
        return await self._fetch_payment(dbc, user, payment_id)


actions = DebtActions()
