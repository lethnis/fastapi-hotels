from datetime import datetime, UTC

from fastapi import Request, Depends
import jwt

from app.exceptions import (
    TokenExpiredException,
    TokenNotFoundException,
    InvalidTokenFormatException,
    UserNotFoundException,
)
from app.config import settings
from app.users.service import UserService


def get_token(request: Request):
    token = request.cookies.get("booking_access_token")
    if token is None:
        raise TokenNotFoundException
    return token


async def get_current_user(token: str = Depends(get_token)):
    try:
        payload = jwt.decode(token, settings.secret_key, settings.algorithm)
    except jwt.PyJWTError:
        raise InvalidTokenFormatException

    expire = payload.get("exp")

    if (expire is None) or (expire < datetime.now(UTC).timestamp()):
        raise TokenExpiredException

    user_id = payload.get("sub")

    if user_id is None:
        raise UserNotFoundException

    user = await UserService.find_by_id(model_id=user_id)

    if user is None:
        raise UserNotFoundException

    return user
