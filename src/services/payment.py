from sqlalchemy.ext.asyncio import AsyncConnection
import sqlalchemy as sa
import logging
import pydantic as pd
import http
from fastapi import HTTPException

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
        return s.Payment.model_validate(
            item,
            from_attributes=True,
            context={"author": s.UserOut(name=item.author_name, email=item.author_email)},
        )

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
        return [(s.Payment.model_validate(
            item,
            from_attributes=True,
            context={"author": s.UserOut(name=item.author_name, email=item.author_email)},
        )) for item in items]

    @staticmethod
    async def get_debt(dbc: AsyncConnection, user: s.User, debt_id: int):
        res = await dbc.execute(
            sa.select(m.debt).where(m.debt.c.id == debt_id)
        )
        return res.first()

    async def create(self, dbc: AsyncConnection, user: s.User, data: s.PaymentCreate):
        # Проверка существования и доступа к займу
        debt = await self.get_debt(dbc, user, data.debt_id)
        if not debt:
            raise HTTPException(
                status_code=http.HTTPStatus.NOT_FOUND,
                detail="Заём не найден"
            )
        
        res = await dbc.execute(
            sa.insert(m.payment)
            .values(
                debt_id=data.debt_id,
                amount=data.amount,
                payment_date=data.payment_date,
                description=data.description,
            )
            .returning(
                m.payment.c.id,
                m.payment.c.debt_id,
                m.payment.c.amount,
                m.payment.c.payment_date,
                m.payment.c.description,
            )
        )
        return s.Payment.model_validate(res.first(), from_attributes=True)

    async def update(
        self, 
        dbc: AsyncConnection, 
        user: s.User, 
        payment_id: int, 
        data: s.PaymentUpdate
    ):
        # Проверка существования и доступа к платежу
        payment = await self.get_one(dbc, user, payment_id)
        if not payment:
            raise HTTPException(
                status_code=http.HTTPStatus.NOT_FOUND,
                detail="Платёж не найден"
            )
        
        # Формируем словарь с обновляемыми полями
        update_data = data.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(
                status_code=http.HTTPStatus.BAD_REQUEST,
                detail="Нет данных для обновления"
            )

        res = await dbc.execute(
            sa.update(m.payment)
            .where(m.payment.c.id == payment_id)
            .values(**update_data)
            .returning(
                m.payment.c.id,
                m.payment.c.debt_id,
                m.payment.c.amount,
                m.payment.c.payment_date,
                m.payment.c.description,
            )
        )
        return s.Payment.model_validate(res.first(), from_attributes=True)

actions = PaymentActions()
