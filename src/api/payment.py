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
    "/payment/{payment_id}/history",
    summary="История платежа",
    description="Вывод истории платежа по его идентификатору",
)
async def get_history(
    payment_id: int,
    user: Annotated[schemas.User, Depends(auth.actions.auth)],
    dbc: AsyncConnection = Depends(get_connection),
):
    return await payment.actions.get_history(dbc, user, payment_id)

