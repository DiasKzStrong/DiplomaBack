from src.core.services.uow import Uow
from ..repository import UserRepository


class AuthUow(Uow):
    user: UserRepository

    repos = (("user", UserRepository),)
