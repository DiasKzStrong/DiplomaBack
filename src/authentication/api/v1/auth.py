from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from ...schemas.user import UserCreateSchema
from ...schemas.auth import LoginResponseSchema, RefreshResponseSchema
from ...services.user_service import UserService
from ...dependencies import (
    get_user_service,
    validate_user_email,
    get_access_from_refresh,
)
from ...exceptions import *

auth_router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/login")


@auth_router.post("/login", response_model=LoginResponseSchema)
async def login(
    user_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    service: Annotated[UserService, Depends(get_user_service)],
):
    user = await service.authenticate_user(user_data.username, user_data.password)

    if not user:
        raise NotAuthenticated()

    tokens = {
        "access_token": service.create_access_token(user.id),
        "refresh_token": service.create_refresh_token(user.id),
    }

    return tokens


@auth_router.post("/register", response_model=int)
async def register(
    service: Annotated[UserService, Depends(get_user_service)],
    user_data: UserCreateSchema = Depends(validate_user_email),
):
    res = await service.create_user(user_data)
    return res


@auth_router.post("/refresh", response_model=RefreshResponseSchema)
async def refresh(new_token: Annotated[str, Depends(get_access_from_refresh)]):
    return {"access_token": new_token}


