from pydantic import BaseModel, EmailStr, field_validator


class User(BaseModel):
    email: EmailStr
    name: str
    admin: bool = False

    @field_validator("email")
    @classmethod
    def convert_to_lowercase(cls, v: str) -> str:
        return v.lower()


class UserReg(User):
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str
