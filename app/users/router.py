from fastapi import APIRouter, status, Response, Depends

from app.exceptions import UserAlreadyExistsException, InvalidCredentialsException
from app.users.models import Users
from app.users.schemas import SUserAuth, SUserResponse
from app.users.service import UserService
from app.users.dependencies import get_current_user
from app.users.auth import get_password_hash, authenticate_user, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth & Users"])


@router.post("/register", status_code=status.HTTP_201_CREATED)
async def register_user(user_data: SUserAuth):

    existing_user = await UserService.find_one_or_none(email=user_data.email)

    if existing_user is not None:
        raise UserAlreadyExistsException

    hashed_password = get_password_hash(user_data.password)
    await UserService.add(email=user_data.email, hashed_password=hashed_password)


@router.post("/login")
async def login_user(response: Response, user_data: SUserAuth):
    user = await authenticate_user(user_data.email, user_data.password)
    if user is None:
        raise InvalidCredentialsException
    access_token = create_access_token({"sub": user.id})
    response.set_cookie("booking_access_token", access_token, httponly=True)
    return access_token


@router.post("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout_user(response: Response):
    response.delete_cookie("booking_access_token")


@router.get("/me")
async def get_users_info(user: Users = Depends(get_current_user)):
    return user


@router.get("/all", response_model=list[SUserResponse])
async def get_all_users(user: Users = Depends(get_current_user)):
    return await UserService.find_all()
