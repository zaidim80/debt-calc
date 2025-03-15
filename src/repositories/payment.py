from datetime import datetime
from sqlalchemy.ext.asyncio import AsyncConnection
import sqlalchemy as sa

import models as m
import schemas as s
from errors import NotFound
from .base import BaseRepository


class PaymentRepository(BaseRepository[s.Payment]):
    def __init__(self):
        super().__init__(m.payment, s.Payment)

    def _build_base_query(self):
        """Построение базового запроса для получения платежа"""
        return (
            self._build_select_query(
                m.payment.c.id,
                m.payment.c.amount,
                m.payment.c.date,
                m.payment.c.month,
                m.user.c.email.label("author_email"),
                m.user.c.name.label("author_name"),
            )
            .select_from(m.payment)
            .join(m.user, m.user.c.email == m.payment.c.author_email)
        )

    async def get_by_id(self, dbc: AsyncConnection, payment_id: int) -> s.Payment:
        """Получение платежа по ID"""
        query = self._build_base_query().where(m.payment.c.id == payment_id)
        result = await self._execute_query(dbc, query)
        item = result.first()
        if not item:
            raise NotFound("Платеж не найден")
        return s.Payment.model_validate(
            item,
            from_attributes=True,
            context={"author": s.UserOut(name=item.author_name, email=item.author_email)},
        )

    async def get_by_debt(self, dbc: AsyncConnection, debt_id: int) -> list[s.Payment]:
        """Получение всех платежей по займу"""
        query = self._build_base_query().where(m.payment.c.debt_id == debt_id)
        result = await self._execute_query(dbc, query)
        return [
            s.Payment.model_validate(
                item,
                from_attributes=True,
                context={"author": s.UserOut(name=item.author_name, email=item.author_email)},
            )
            for item in result.fetchall()
        ]

    async def get_by_debt_and_month(
        self, dbc: AsyncConnection, debt_id: int, month: str
    ) -> s.Payment | None:
        """Получение платежа по займу и месяцу"""
        query = self._build_base_query().where(
            m.payment.c.debt_id == debt_id,
            m.payment.c.month == month,
        )
        result = await self._execute_query(dbc, query)
        item = result.first()
        if not item:
            return None
        return s.Payment.model_validate(
            item,
            from_attributes=True,
            context={"author": s.UserOut(name=item.author_name, email=item.author_email)},
        )

    async def create(
        self, dbc: AsyncConnection, debt_id: int, amount: int, month: str, author_email: str
    ) -> int:
        """Создание нового платежа"""
        query = self._build_insert_query({
            "debt_id": debt_id,
            "amount": amount,
            "date": datetime.now(),
            "month": month,
            "author_email": author_email,
        }).returning(m.payment.c.id)
        result = await self._execute_query(dbc, query)
        return result.scalar()

    async def update(self, dbc: AsyncConnection, payment_id: int, amount: int) -> None:
        """Обновление суммы платежа"""
        query = self._build_update_query(
            m.payment.c.id == payment_id,
            {"amount": amount}
        )
        await self._execute_query(dbc, query)


class PaymentLogRepository(BaseRepository[s.PaymentLog]):
    def __init__(self):
        super().__init__(m.pay_log, s.PaymentLog)

    def _build_base_query(self):
        """Построение базового запроса для получения лога платежей"""
        return (
            self._build_select_query(
                m.pay_log.c.id,
                m.pay_log.c.date,
                m.pay_log.c.amount,
                m.user.c.email.label("author_email"),
                m.user.c.name.label("author_name"),
            )
            .select_from(m.pay_log)
            .outerjoin(m.user, m.user.c.email == m.pay_log.c.author_email)
        )

    async def get_by_payment(self, dbc: AsyncConnection, payment_id: int) -> list[s.PaymentLog]:
        """Получение истории платежа"""
        query = self._build_base_query().where(m.pay_log.c.payment_id == payment_id)
        result = await self._execute_query(dbc, query)
        return [
            s.PaymentLog.model_validate(
                item,
                from_attributes=True,
                context={
                    "author": s.Author.model_validate(item, from_attributes=True)
                    if item.author_email else None
                },
            )
            for item in result.fetchall()
        ]

    async def create(
        self, dbc: AsyncConnection, payment_id: int, amount: int, author_email: str
    ) -> None:
        """Создание записи в логе платежей"""
        query = self._build_insert_query({
            "payment_id": payment_id,
            "amount": amount,
            "author_email": author_email,
            "date": datetime.now(),
        })
        await self._execute_query(dbc, query)


payment_repository = PaymentRepository()
payment_log_repository = PaymentLogRepository() 