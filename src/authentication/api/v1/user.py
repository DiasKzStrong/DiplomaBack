from fastapi import APIRouter, Depends
from ...schemas.user import UserReadSchema
from ...schemas.auth import JWTData
from ...dependencies import get_current_user


user_router = APIRouter()


@user_router.get("/me", response_model=UserReadSchema)
async def user_me(user: UserReadSchema = Depends(get_current_user)):
    return user
