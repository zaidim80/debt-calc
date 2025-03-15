from pydantic import BaseModel, field_validator, model_validator, Field
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


class Author(BaseModel):
    email: str | None = Field(default=None, alias="author_email")
    name: str | None = Field(default=None, alias="author_name")


class Authored(BaseModel):
    author: UserOut | None = None

    @model_validator(mode="after")
    @classmethod
    def check_author(cls, v, info):
        v.author = info.context["author"] if info.context and "author" in info.context else None
        return v


class UserReg(User):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class Debt(Authored):
    id: int | None
    amount: int
    date: datetime
    name: str
    period: int
    rate: float
    default_payment: int = 0


class Payment(Authored):
    id: int | None = None
    amount: int
    date: datetime
    month: str


class FuturePayment(BaseModel):
    id: int | None = None
    default: int = 0
    amount: int = 0
    interest: int = 0
    redemption: int = 0
    total: int = 0
    remainder: int = 0
    date: str
    payment_id: int | None = None


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


class PaymentLog(Authored):
    id: int
    date: datetime
    amount: Decimal
