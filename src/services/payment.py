from sqlalchemy.ext.asyncio import AsyncConnection
import sqlalchemy as sa
import logging

import schemas as s
import models as m
from errors import NotFound


log = logging.getLogger()


class PaymentActions:
    @staticmethod
    async def get_history(dbc: AsyncConnection, user: s.User, item_id: int) -> list[s.PaymentLog]:
        res = await dbc.execute(
            sa.select(
                m.payment.c.id,
                m.payment.c.date,
                m.payment.c.amount,
            )
            .select_from(m.payment)
            .where(m.payment.c.id == item_id)
        )
        payment = res.first()
        if payment is None:
            raise NotFound("Платеж не найден")
        res = await dbc.execute(
            sa.select(
                m.pay_log.c.id,
                m.pay_log.c.date,
                m.pay_log.c.amount,
                m.user.c.email.label("author_email"),
                m.user.c.name.label("author_name"),
            )
            .select_from(m.pay_log)
            .outerjoin(m.user, m.user.c.email == m.pay_log.c.author_email)
            .where(m.pay_log.c.payment_id == payment.id)
        )
        items = res.fetchall()
        return [s.PaymentLog.model_validate(
            item,
            from_attributes=True,
            context={
                "author": s.Author.model_validate(item, from_attributes=True) if item.author_email else None
            },
        ) for item in items]


actions = PaymentActions()
