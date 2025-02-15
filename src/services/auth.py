from sqlalchemy.ext.asyncio import AsyncConnection
import sqlalchemy as sa
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi import HTTPException, Depends
import hashlib
import http
from typing import Annotated
import logging
from datetime import datetime, timedelta, timezone
import jwt

import schemas as s
import models as m
from db import dbe
from config import cfg


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
log = logging.getLogger()


class AuthActions:
    @staticmethod
    def hash_password(pwd: str) -> str:
        return hashlib.sha256(pwd.encode()).hexdigest()
    
    @staticmethod
    def create_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(days=30)
        to_encode.update({"exp": expire})
        token = jwt.encode(to_encode, cfg.auth_secret, algorithm="HS256")
        return token

    async def register_user(self, dbc: AsyncConnection, data: s.UserReg) -> s.User | None:
        pass_hash = self.hash_password(data.password)
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

    async def get_token(self, dbc: AsyncConnection, data: OAuth2PasswordRequestForm) -> s.Token:
        pass_hash = self.hash_password(data.password)
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
                detail="Неверный email или пароль",  # Изменяем сообщение об ошибке для безопасности
                status_code=http.HTTPStatus.UNAUTHORIZED,  # Меняем код ответа на более подходящий
            )
        if user.password != pass_hash:
            log.error("Неверная эл. почта или пароль")
            raise HTTPException(
                detail="Неверный email или пароль",
                status_code=http.HTTPStatus.UNAUTHORIZED,
            )
        token = s.Token(
            access_token=self.create_token({
                "email": user.email,
                "admin": user.admin,
            }),
            token_type="bearer",
        )
        return token

    @staticmethod
    async def auth(
        token: Annotated[str, Depends(oauth2_scheme)],
    ) -> s.User:
        try:
            payload = jwt.decode(token, cfg.auth_secret, algorithms=["HS256", ])
        except Exception as e:
            log.error(f"Токен не валидный: {e}")
            raise HTTPException(
                status_code=http.HTTPStatus.UNAUTHORIZED,
                detail=f"Токен не валидный: {e}",
                headers={"WWW-Authenticate": "Bearer"},
            )
        email = payload.get("email")
        if email is None:
            log.error("Токен не найден или не зарегистрирован")
            raise HTTPException(
                detail="Токен не найден или не зарегистрирован",
                status_code=http.HTTPStatus.UNAUTHORIZED,
                headers={"WWW-Authenticate": "Bearer"},
            )
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
                log.error(f"Ошибка авторизации, пользователь {email} не найден")
                raise HTTPException(
                    detail="Ошибка авторизации, пользователь {email} не найден",
                    status_code=http.HTTPStatus.UNAUTHORIZED,
                )
            log.info(f"Авторизован, как {email}")
            return s.User.model_validate(user, from_attributes=True)


actions = AuthActions()
