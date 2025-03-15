from typing import Annotated
from fastapi import APIRouter, Depends, Query
from fastapi.security import OAuth2PasswordRequestForm

import logging
import http
from sqlalchemy.ext.asyncio import AsyncConnection

from db import get_connection
import schemas
from services import auth
from services.debt import service as debt_service


router = APIRouter()
log = logging.getLogger()


@router.get(
    "/debt",
    status_code=http.HTTPStatus.OK,
    description="Список займов",
    response_model=list[schemas.Debt]
)
async def get_list(
    user: Annotated[schemas.User, Depends(auth.actions.auth)],
    dbc: AsyncConnection = Depends(get_connection),
):
    return await debt_service.get_list(dbc, user)


@router.get(
    "/debt/{debt_id}",
    status_code=http.HTTPStatus.OK,
    description="Займ",
    response_model=schemas.DebtInfo
)
async def get_one(
    debt_id: int,
    user: Annotated[schemas.User, Depends(auth.actions.auth)],
    dbc: AsyncConnection = Depends(get_connection),
):
    return await debt_service.get_one(dbc, user, debt_id)


@router.post(
    "/debt/{debt_id}/pay",
    status_code=http.HTTPStatus.OK,
    description="Платеж",
    response_model=schemas.DebtInfo
)
async def process_payment(
    debt_id: int,
    payment: schemas.PaymentPay,
    user: Annotated[schemas.User, Depends(auth.actions.auth)],
    dbc: AsyncConnection = Depends(get_connection),
):
    return await debt_service.process_payment(dbc, user, debt_id, payment)
