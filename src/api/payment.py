from typing import Annotated
from fastapi import APIRouter, Depends, Query
import http

import logging
from sqlalchemy.ext.asyncio import AsyncConnection

from db import get_connection
import schemas
from services import payment, auth


router = APIRouter()
log = logging.getLogger()


@router.get(
    "/payment/{payment_id}",
    summary="Платеж",
    description="Вывод данных конкретного платежа по его идентификатору",
)
async def get_one(
    payment_id: int,
    user: Annotated[schemas.User, Depends(auth.actions.auth)],
    dbc: AsyncConnection = Depends(get_connection),
):
    return payment.actions.get_one(dbc, user, payment_id)


@router.get(
    "/payment/",
    summary="Список платежей",
    description="Вывод списка платежей с фильтром по идентификатору займа",
)
async def get_list(
    user: Annotated[schemas.User, Depends(auth.actions.auth)],
    dbc: AsyncConnection = Depends(get_connection),
    debt_id: Annotated[int | None, Query(alias="debt")] = None,
):
    return payment.actions.get_list(dbc, user, debt_id)


@router.post(
    "/payment/",
    summary="Создание платежа",
    description="Создание нового платежа по займу",
    status_code=http.HTTPStatus.CREATED,
)
async def create(
    data: schemas.PaymentCreate,
    user: Annotated[schemas.User, Depends(auth.actions.auth)],
    dbc: AsyncConnection = Depends(get_connection),
):
    return await payment.actions.create(dbc, user, data)


@router.patch(
    "/payment/{payment_id}",
    summary="Изменение платежа",
    description="Изменение существующего платежа по его идентификатору",
)
async def update(
    payment_id: int,
    data: schemas.PaymentUpdate,
    user: Annotated[schemas.User, Depends(auth.actions.auth)],
    dbc: AsyncConnection = Depends(get_connection),
):
    return await payment.actions.update(dbc, user, payment_id, data)
