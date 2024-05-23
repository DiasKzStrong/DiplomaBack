from .auth import auth_router
from .user import user_router
from fastapi import APIRouter

v1_auth_router = APIRouter()
v1_auth_router.include_router(auth_router, prefix="/auth", tags=["auth"])
v1_auth_router.include_router(user_router, prefix="/users", tags=["users"])
