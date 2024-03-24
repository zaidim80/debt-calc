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
    description="Получение токена",
)
async def login(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    dbc: AsyncConnection = Depends(get_connection),
):
    token = await auth.actions.get_token(dbc, form_data)
    return token


# @router.post(
#     "/register",
#     status_code=http.HTTPStatus.CREATED,
#     response_model=schemas.User,
#     description="Регистрация пользователя",
# )
# async def register(
#     form_data: schemas.UserReg,
#     dbc: AsyncConnection = Depends(get_connection),
# ):
#     log.info(f"Вызов метода регистрации пользователя с параметрами: {form_data}")
#     user = await auth.actions.register_user(dbc, form_data)
#     return user


@router.get("/me")
async def get_me(user: Annotated[schemas.User, Depends(auth.actions.auth)]):
    return user
