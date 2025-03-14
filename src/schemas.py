from pydantic import BaseModel, field_validator, model_validator
from datetime import datetime, date
from decimal import Decimal


class User(BaseModel):
    email: str
    name: str
    admin: bool = False

    @field_validator("email")
    @classmethod
    def convert_to_lowercase(cls, v: str) -> str:
        return v.lower()


class UserOut(BaseModel):
    email: str
    name: str


class UserReg(User):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class Debt(BaseModel):
    id: int | None
    amount: int
    date: datetime
    name: str
    period: int
    rate: float
    author: UserOut | None = None
    default_payment: int = 0

    @model_validator(mode="after")
    @classmethod
    def check_author(cls, v, info):
        if isinstance(info.context, dict) and "author" in info.context:
            v.author = info.context["author"]
        return v


class Payment(BaseModel):
    id: int | None = None
    amount: int
    date: datetime
    month: str
    author: UserOut | None = None

    @model_validator(mode="after")
    @classmethod
    def check_author(cls, v, info):
        if isinstance(info.context, dict) and "author" in info.context:
            v.author = info.context["author"]
        return v


class FuturePayment(BaseModel):
    id: int | None = None
    default: int = 0
    amount: int = 0
    interest: int = 0
    redemption: int = 0
    total: int = 0
    remainder: int = 0
    date: str


class DebtInfo(Debt):
    schedule: list[FuturePayment] | None = None


class PaymentCreate(BaseModel):
    debt_id: int
    amount: Decimal
    payment_date: date
    description: str | None = None


class PaymentUpdate(BaseModel):
    amount: Decimal | None = None
    payment_date: date | None = None
    description: str | None = None


class PaymentPay(BaseModel):
    amount: Decimal
    month: str
    description: str | None = None
