import datetime

from pydantic import BaseModel, Field, ConfigDict

class JWTData(BaseModel):
    id: int = Field(alias="sub")
    exp: datetime.datetime
    iat: datetime.datetime


class LoginResponseSchema(BaseModel):
    access_token: str
    refresh_token: str

class RefreshTokenSchema(BaseModel):
    refresh_token: str

class RefreshResponseSchema(BaseModel):
    access_token: str
