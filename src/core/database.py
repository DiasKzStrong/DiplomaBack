from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import declarative_base, Mapped, mapped_column
from sqlalchemy import func
from datetime import datetime
from .conf import settings


engine = create_async_engine(url=settings.POSTGRES_URL)

DEFAULT_SESSION_MAKER = async_sessionmaker(bind=engine)

Base = declarative_base()


class BaseModel(Base):
    __abstract__ = True

    created_at: Mapped[datetime] = mapped_column(server_default=func.now())
    updated_at: Mapped[datetime] = mapped_column(default=datetime.now())
