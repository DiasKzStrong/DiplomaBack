from sqlalchemy.ext.asyncio import AsyncSession

from .schemas.user import UserCreateSchema
from .models import User
from sqlalchemy import insert, select, update, delete


class UserRepository:
    model = User

    def __init__(self, session: AsyncSession):
        self.session = session

    async def create(self, user: UserCreateSchema):
        query = insert(self.model).values(**user.model_dump()).returning(self.model.id)
        res = await self.session.scalars(query)
        return res.first()

    async def get(self, user_id: int):
        query = select(self.model).filter_by(id=user_id)
        res = await self.session.scalars(query)
        return res.first()

    async def get_by_filters(self, **filters):
        query = select(self.model).filter_by(**filters)
        res = await self.session.scalars(query)
        return res.first()

    async def update(self, user_id: int, user: UserCreateSchema):
        query = update(self.model).values(**user.model_dump()).returning(self.model.id)
        res = await self.session.execute(query)
        return res.first()

    async def delete(self, user_id: int):
        query = delete(self.model).filter_by(id=user_id).returning(self.model.id)
        res = await self.session.execute(query)
        return res.first()
