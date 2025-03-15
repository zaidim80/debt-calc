from datetime import datetime
import math
import schemas as s


class PaymentScheduleCalculator:
    @staticmethod
    def calc_default_payment(rate: float, period: int, debt: float) -> int:
        """Расчет ежемесячного платежа"""
        return round(debt * (rate + rate / (pow(1 + rate, period) - 1))) if debt > 0 else 0

    def get_schedule(self, debt: s.Debt, payments: list[s.Payment]) -> list[s.FuturePayment]:
        """Расчет графика платежей"""
        payments_dict = {item.month: item for item in payments}
        monthly_rate = debt.rate / 12 / 100
        default_payment = self.calc_default_payment(monthly_rate, debt.period, debt.amount)
        
        month = debt.date.month - 1
        year = debt.date.year
        loan_paid = 0
        loan_debt = debt.amount
        now = datetime.now()
        today = f"{now.year}-{now.month:02d}"
        month_new_payment = default_payment
        schedule = []

        for i in range(1, debt.period + 1):
            month += 1
            current_month = month % 12 + 1
            current_year = year + math.floor(month / 12)
            month_id = f"{current_year:04d}-{current_month:02d}"
            
            schedule_item = self._calc_month_payment(
                i, month_id, monthly_rate, loan_debt, loan_paid,
                payments_dict, today, default_payment, month_new_payment,
                debt.period
            )
            
            loan_paid = schedule_item.total
            loan_debt = schedule_item.remainder
            month_new_payment = self.calc_default_payment(monthly_rate, debt.period - i, loan_debt)
            
            schedule.append(schedule_item)
        
        return schedule

    def _calc_month_payment(
        self,
        month_num: int,
        month_id: str,
        monthly_rate: float,
        loan_debt: float,
        loan_paid: float,
        payments: dict,
        today: str,
        default_payment: float,
        current_payment: float,
        total_period: int,
    ) -> s.FuturePayment:
        """Расчет платежа за конкретный месяц"""
        month_payed = month_id in payments
        loan_debt *= 1 + monthly_rate
        month_tax = loan_debt * monthly_rate

        if month_payed:
            payment = payments[month_id]
            month_payment = payment.amount
            loan_paid += month_payment
            loan_debt -= month_payment
            rec_payment = default_payment
            payed_summ = month_payment
            payment_id = payment.id
        elif today > month_id:
            month_payment = 0
            rec_payment = current_payment
            payed_summ = 0
            payment_id = None
        else:
            month_payment = current_payment
            loan_debt -= month_payment
            rec_payment = month_payment
            payed_summ = 0
            payment_id = None

        return s.FuturePayment(
            id=month_num,
            default=rec_payment,
            amount=payed_summ,
            interest=round(month_tax),
            redemption=round(month_payment - month_tax),
            total=round(loan_paid),
            remainder=round(loan_debt),
            date=month_id,
            payment_id=payment_id
        )


calculator = PaymentScheduleCalculator()
