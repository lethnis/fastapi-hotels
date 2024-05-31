from datetime import datetime, timedelta, UTC
from pydantic import EmailStr
import jwt
from passlib.context import CryptContext

from app.config import settings
from app.users.service import UserService

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_access_token(data: dict) -> str:
    to_encode = data.copy()
    expire = datetime.now(UTC) + timedelta(minutes=30)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.secret_key, settings.algorithm)
    return encoded_jwt


async def authenticate_user(email: EmailStr, password: str):

    user = await UserService.find_one_or_none(email=email)
    if (user is None) or (not verify_password(password, user.hashed_password)):
        return None
    return user
