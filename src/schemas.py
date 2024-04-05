from pydantic import BaseModel, EmailStr, field_validator
from datetime import datetime


class User(BaseModel):
    email: EmailStr
    name: str
    admin: bool = False

    @field_validator("email")
    @classmethod
    def convert_to_lowercase(cls, v: str) -> str:
        return v.lower()


class UserOut(BaseModel):
    email: EmailStr
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


class Payment(BaseModel):
    id: int | None = None
    amount: int
    date: datetime
    author: UserOut | None = None
    debt: Debt | None = None
