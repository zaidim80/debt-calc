from sqlalchemy.ext.asyncio import AsyncConnection
import logging

import schemas as s
from repositories.payment import payment_repository, payment_log_repository


log = logging.getLogger()


class PaymentService:
    async def fetch_payments(self, dbc: AsyncConnection, debt_id: int) -> list[s.Payment]:
        """Получение всех платежей по займу"""
        return await payment_repository.get_by_debt(dbc, debt_id)

    async def fetch_payment(self, dbc: AsyncConnection, payment_id: int) -> s.Payment:
        """Получение конкретного платежа"""
        return await payment_repository.get_by_id(dbc, payment_id)

    async def create_payment(
        self,
        dbc: AsyncConnection,
        user: s.User,
        debt_id: int,
        payment: s.PaymentUpdate
    ) -> int:
        """Создание нового платежа"""
        return await payment_repository.create(
            dbc,
            debt_id=debt_id,
            amount=payment.amount,
            month=payment.month,
            author_email=user.email,
        )

    async def update_payment(
        self,
        dbc: AsyncConnection,
        payment_id: int,
        amount: int
    ) -> None:
        """Обновление существующего платежа"""
        await payment_repository.update(dbc, payment_id, amount)

    async def create_payment_log(
        self,
        dbc: AsyncConnection,
        user: s.User,
        payment_id: int,
        amount: int
    ) -> None:
        """Создание записи в логе платежей"""
        await payment_log_repository.create(
            dbc,
            payment_id=payment_id,
            amount=amount,
            author_email=user.email,
        )

    async def get_history(self, dbc: AsyncConnection, user: s.User, item_id: int) -> list[s.PaymentLog]:
        """Получение истории платежа"""
        payment = await self.fetch_payment(dbc, item_id)
        return await payment_log_repository.get_by_payment(dbc, payment.id)


payment_service = PaymentService()
