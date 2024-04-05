from sqlalchemy.ext.asyncio import AsyncConnection
import sqlalchemy as sa
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import HTTPException, Depends
import hashlib
import http
from typing import Annotated
import logging

import schemas as s
import models as m
from db import rds, dbe


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
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


actions = PaymentActions()
