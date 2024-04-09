from typing import Annotated
from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm

import logging
import http
from sqlalchemy.ext.asyncio import AsyncConnection

from db import get_connection
import schemas
from services import auth


router = APIRouter()
log = logging.getLogger()


@router.post(
    "/token",
    status_code=http.HTTPStatus.OK,
    summary="Получение токена",
    description="Получение токена (авторизация по логину и паролю)",
)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    dbc: AsyncConnection = Depends(get_connection),
):
    token = await auth.actions.get_token(dbc, form_data)
    return token


@router.get(
    "/me",
    status_code=http.HTTPStatus.OK,
    summary="Авторизованный",
    description="Вывод данных авторизованного пользователя",
)
async def get_me(user: Annotated[schemas.User, Depends(auth.actions.auth)]):
    return user
