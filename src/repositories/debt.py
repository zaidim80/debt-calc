from sqlalchemy.ext.asyncio import AsyncConnection
import sqlalchemy as sa

import models as m
import schemas as s
from errors import NotFound
from .base import BaseRepository


class DebtRepository(BaseRepository[s.DebtInfo]):
    def __init__(self):
        super().__init__(m.debt, s.DebtInfo)

    def _build_base_query(self):
        """Построение базового запроса для получения займа"""
        return (
            self._build_select_query(
                m.debt.c.id,
                m.debt.c.name,
                m.debt.c.date,
                m.debt.c.amount,
                m.debt.c.period,
                m.debt.c.rate,
                m.user.c.email.label("author_email"),
                m.user.c.name.label("author_name"),
            )
            .select_from(m.debt)
            .join(m.user, m.user.c.email == m.debt.c.author_email)
        )

    async def get_by_id(self, dbc: AsyncConnection, debt_id: int) -> s.DebtInfo:
        """Получение займа по ID"""
        query = self._build_base_query().where(m.debt.c.id == debt_id)
        result = await self._execute_query(dbc, query)
        item = result.first()
        if not item:
            raise NotFound("Займ не найден")
        return s.DebtInfo.model_validate(
            item,
            from_attributes=True,
            context={"author": s.UserOut(name=item.author_name, email=item.author_email)},
        )

    async def get_all(self, dbc: AsyncConnection) -> list[s.Debt]:
        """Получение списка всех займов"""
        query = self._build_base_query().order_by(m.debt.c.date)
        result = await self._execute_query(dbc, query)
        return [
            s.Debt.model_validate(
                item,
                from_attributes=True,
                context={"author": s.UserOut(name=item.author_name, email=item.author_email)},
            )
            for item in result.fetchall()
        ]


debt_repository = DebtRepository() 