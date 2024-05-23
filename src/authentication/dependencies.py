from datetime import datetime
from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from functools import cache
from .schemas.user import UserCreateSchema
from .schemas.auth import JWTData,RefreshTokenSchema
from .services.user_service import UserService
from .conf import auth_settings
from jose import jwt, JWTError
from .exceptions import EmailTaken, InvalidToken, NotAuthenticated, TimeExpired

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@cache
def get_user_service():
    return UserService()


def get_token_payload(token: str, secret_key: str):
    if not token:
        raise NotAuthenticated()

    try:
        payload = jwt.decode(token, secret_key, algorithms=[auth_settings.ALGORITHM])
    except JWTError as e:
        raise InvalidToken()

    return JWTData(**payload)


def parse_access_token_jwt(token: str = Depends(oauth2_scheme)):
    payload = get_token_payload(token, auth_settings.JWT_ACCESS_SECRET_KEY)
    return payload


def parse_refresh_token_jwt(token: RefreshTokenSchema):
    payload = get_token_payload(token.refresh_token, auth_settings.JWT_REFRESH_SECRET_KEY)
    return payload


def get_access_from_refresh(
    token: JWTData = Depends(parse_refresh_token_jwt),
    service: UserService = Depends(get_user_service),
):
    access_token = service.create_access_token(id=token.id)

    return access_token


async def get_current_user(
    token: JWTData = Depends(parse_access_token_jwt),
    service: UserService = Depends(get_user_service),
):
    user = await service.get_user(user_id=token.id)

    return user


async def validate_user_email(user: UserCreateSchema):
    service = get_user_service()
    if await service.get_user_by_email(user.email):
        raise EmailTaken()

    return user
