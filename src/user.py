import argparse
import asyncio
import getpass
import sys
from typing import Optional

from sqlalchemy.ext.asyncio import AsyncEngine

from db import dbe
from models import user
from services.auth import actions


async def create_user(
    dbe: AsyncEngine,
    email: str,
    name: str,
    is_admin: bool = False,
    password: Optional[str] = None
) -> None:
    """
    Создает нового пользователя с указанными параметрами.
    Запрашивает пароль интерактивно, если он не указан.
    """
    if not password:
        password = getpass.getpass("Введите пароль: ")
        password_confirm = getpass.getpass("Подтвердите пароль: ")
        
        if password != password_confirm:
            print("Ошибка: пароли не совпадают")
            sys.exit(1)

    async with dbe.begin() as dbc:
        try:
            await dbc.execute(
                user.insert().values(
                    email=email,
                    name=name,
                    admin=is_admin,
                    password=actions.hash_password(password),
                )
            )
            print(f"Пользователь {email} успешно создан")
        
        except Exception as e:
            print(f"Ошибка при создании пользователя: {e}")
            sys.exit(1)


async def async_main() -> None:
    parser = argparse.ArgumentParser(description="Создание нового пользователя")
    parser.add_argument("--email", required=True, help="Email пользователя")
    parser.add_argument("--name", required=True, help="Имя пользователя")
    parser.add_argument("--admin", action="store_true", help="Сделать пользователя администратором")
    
    args = parser.parse_args()
    
    await create_user(
        dbe=dbe,
        email=args.email,
        name=args.name,
        is_admin=args.admin
    )
    await dbe.dispose()


def main() -> None:
    asyncio.run(async_main())


if __name__ == "__main__":
    main() 