from datetime import datetime, timedelta
from src.authentication.conf import auth_settings
from jose import jwt
from .uow import AuthUow
from ..schemas.user import UserCreateSchema, UserReadSchema
from ..utils import verify_password, get_password_hash


class UserService:
    def __init__(self):
        self.uow = AuthUow

    async def get_user(self, user_id: int):
        async with self.uow() as uow:
            res = await uow.user.get(user_id)
            return res

    async def get_user_by_email(self, email: str):
        async with self.uow() as uow:
            res = await uow.user.get_by_filters(email=email)
            return res

    async def create_user(self, user: UserCreateSchema) -> int:
        async with self.uow() as uow:
            user.password = get_password_hash(user.password)
            res = await uow.user.create(user)
            await uow.commit()
            return res

    async def update_user(self, user: UserCreateSchema, user_id: int):
        async with self.uow() as uow:
            res = await uow.user.update(user_id=user_id, user=user)
            await uow.commit()
            return res

    async def delete_user(self, user_id: int):
        async with self.uow() as uow:
            res = await uow.user.delete(user_id=user_id)
            await uow.commit()
            return res

    def create_access_token(
        self, id: str | int, expires_delta: timedelta = None
    ) -> str:
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=auth_settings.ACCESS_TOKEN_EXPIRE_MINUTES
            )

        payload = {
            "exp": expire,
            "iat": datetime.utcnow(),
            "sub": str(id),
        }

        return jwt.encode(
            payload,
            auth_settings.JWT_ACCESS_SECRET_KEY,
            algorithm=auth_settings.ALGORITHM,
        )

    def create_refresh_token(
        self, id: str | int, expires_delta: timedelta = None
    ) -> str:
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(
                minutes=auth_settings.REFRESH_TOKEN_EXPIRE_MINUTES
            )

        payload = {
            "exp": expire,
            "iat": datetime.utcnow(),
            "sub": str(id),
        }

        return jwt.encode(
            payload,
            auth_settings.JWT_REFRESH_SECRET_KEY,
            algorithm=auth_settings.ALGORITHM,
        )

    async def authenticate_user(self, email: str, password: str):
        async with self.uow() as uow:
            user = await uow.user.get_by_filters(email=email)
            if not user:
                return False
            if not verify_password(password, user.password):
                return False

            return user
