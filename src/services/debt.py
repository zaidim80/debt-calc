from sqlalchemy.ext.asyncio import AsyncConnection
from fastapi.security import OAuth2PasswordBearer
import logging

import schemas as s
from errors import AccessDenied
from repositories.debt import debt_repository
from repositories.payment import payment_repository
from .payment_calculator import calculator
from .payment import payment_service

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
log = logging.getLogger()


class DebtService:
    async def get_one(self, dbc: AsyncConnection, user: s.User, item_id: int) -> s.DebtInfo:
        """Получение информации о займе с графиком платежей"""
        # получаем займ
        result = await debt_repository.get_by_id(dbc, user, item_id)
        # рекомендуемый платеж
        result.default_payment = calculator.get_default_payment(result)
        # получаем платежи
        payments = await payment_service.fetch_payments(dbc, item_id)
        # рассчитываем график платежей
        result.schedule = calculator.get_schedule(result, payments)
        return result

    async def get_list(self, dbc: AsyncConnection, user: s.User) -> list[s.Debt]:
        """Получение списка всех займов"""
        return await debt_repository.get_all(dbc, user)

    async def process_payment(
        self,
        dbc: AsyncConnection,
        user: s.User,
        debt_id: int,
        payment: s.PaymentUpdate,
    ) -> s.DebtInfo:
        """Обработка платежа по займу"""
        # проверка прав доступа
        if not user.admin:
            raise AccessDenied()
            
        # проверяем, что займ существует
        debt = await debt_repository.get_by_id(dbc, debt_id)
        
        # ищем существующий платеж за этот месяц
        existing_payment = await payment_repository.get_by_debt_and_month(dbc, debt_id, payment.month)
        
        if existing_payment:
            # обновляем существующий платеж
            await payment_service.update_payment(dbc, existing_payment.id, payment.amount)
            payment_id = existing_payment.id
        else:
            # создаем новый платеж
            payment_id = await payment_service.create_payment(dbc, user, debt_id, payment)
            
        # создаем запись в логе
        await payment_service.create_payment_log(dbc, user, payment_id, payment.amount)
        
        # получаем обновленный список платежей
        payments = await payment_service.fetch_payments(dbc, debt_id)
        
        # обновляем график платежей
        debt.schedule = calculator.get_schedule(debt, payments)
        return debt


service = DebtService()
