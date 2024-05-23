from src.core.database import BaseModel
from sqlalchemy import BigInteger, Identity
from sqlalchemy.orm import Mapped, mapped_column


class User(BaseModel):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(
        BigInteger, Identity(always=True, start=1), primary_key=True
    )
    username: Mapped[str]
    email: Mapped[str]
    password: Mapped[str]
