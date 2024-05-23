from src.core.exceptions import DetailedException
from fastapi import status
from .constants import ErrorDetail


class NotAuthenticated(DetailedException):
    STATUS_CODE = status.HTTP_401_UNAUTHORIZED
    DETAIL = ErrorDetail.AUTHENTICATION_FAILED

    def __init__(self):
        super().__init__(headers={"WWW-Authenticate": "Bearer"})


class UserNotFound(DetailedException):
    STATUS_CODE = status.HTTP_404_NOT_FOUND
    DETAIL = ErrorDetail.USER_NOT_FOUND


class EmailTaken(NotAuthenticated):
    DETAIL = ErrorDetail.EMAIL_TAKEN


class InvalidToken(NotAuthenticated):
    DETAIL = ErrorDetail.INVALID_TOKEN


class TimeExpired(NotAuthenticated):
    DETAIL = ErrorDetail.ACCESS_TOKEN_EXPIRED
