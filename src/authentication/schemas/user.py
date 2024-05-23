from datetime import datetime

from pydantic import BaseModel, EmailStr, ConfigDict


## user related schemas
class UserReadSchema(BaseModel):
    id: int
    email: EmailStr
    username: str
    created_at: datetime
    updated_at: datetime


class UserCreateSchema(BaseModel):
    email: EmailStr
    password: str
    username: str


class UserUpdateSchema(BaseModel):
    email: EmailStr | None
    password: str | None
    name: str | None
