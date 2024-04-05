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


class AuthActions:
    @staticmethod
    async def register_user(dbc: AsyncConnection, data: s.UserReg) -> s.User | None:
        pass_hash = hashlib.sha1(data.password.encode()).hexdigest()
        res = await dbc.execute(
            sa.select(m.user.c.email)
            .select_from(m.user)
            .where(m.user.c.email == data.email)
        )
        existing_user = res.first()
        if existing_user:
            log.error(f"Пользователь с эл. почтой {data.email} уже зарегистрирован")
            raise HTTPException(
                detail="Пользователь с указанной эл. почтой уже зарегистрирован",
                status_code=http.HTTPStatus.BAD_REQUEST,
            )
        res = await dbc.execute(
            sa.insert(m.user)
            .values(
                **data.model_dump(exclude={"password"}),
                password=pass_hash,
            )
            .returning(
                m.user.c.email,
                m.user.c.name,
                m.user.c.admin,
            )
        )
        return s.User.model_validate(res.first(), from_attributes=True)

    @staticmethod
    async def get_token(dbc: AsyncConnection, data: OAuth2PasswordRequestForm) -> s.Token:
        pass_hash = hashlib.sha1(data.password.encode()).hexdigest()
        res = await dbc.execute(
            sa.select(
                m.user.c.email,
                m.user.c.password,
                m.user.c.admin,
            )
            .select_from(m.user)
            .where(m.user.c.email == data.username.lower())
        )
        user = res.first()
        if user is None:
            log.error(f"Пользователь с указанной эл. почтой {data.username} не найден")
            raise HTTPException(
                detail="Пользователь с указанной эл. почтой не найден",
                status_code=http.HTTPStatus.BAD_REQUEST,
            )
        if user.password != pass_hash:
            log.error("Неверная эл. почта или пароль")
            raise HTTPException(
                detail="Неверная эл. почта или пароль",
                status_code=http.HTTPStatus.BAD_REQUEST,
            )
        # логика формирования токена заведомо небезопасная
        token = s.Token(
            access_token=hashlib.sha1(str(user.id).encode()).hexdigest(),
            token_type="bearer",
        )
        await rds.set(f"token-{token.access_token}", user.email, 3600)
        return token

    @staticmethod
    async def auth(
        token: Annotated[str, Depends(oauth2_scheme)],
    ) -> s.User:
        email = str(await rds.get(f"token-{token}"))
        if email is None:
            log.error("Токен не найден или не зарегистрирован")
            raise HTTPException(
                detail="Токен не найден или не зарегистрирован",
                status_code=http.HTTPStatus.UNAUTHORIZED,
                headers={"WWW-Authenticate": "Bearer"},
            )
        await rds.set(f"token-{token}", email, 3600)
        async with dbe.begin() as dbc:
            res = await dbc.execute(
                sa.select(
                    m.user.c.email,
                    m.user.c.name,
                    m.user.c.admin,
                )
                .select_from(m.user)
                .where(m.user.c.email == email)
            )
            user = res.first()
            if user is None:
                log.error("Ошибка авторизации, пользователь не найден")
                raise HTTPException(
                    detail="Ошибка авторизации, пользователь не найден",
                    status_code=http.HTTPStatus.BAD_REQUEST,
                )
            log.info(f"Авторизован, как {email}")
            return s.User.model_validate(user, from_attributes=True)


actions = AuthActions()
