from uuid import UUID
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from schemas.users import UserRegisterSchema, UserLoginSchema, UserTokenInfoSchema
from services.users import UserService, decoded_jwt

user_router = APIRouter(
    prefix="/user",
    tags=["Пользователи"]
)

oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/user/login",
)

def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decoded_jwt(token)
    user_id: UUID = payload.get("id")
    return user_id

@user_router.post("/register")
async def register_user(register_data: UserRegisterSchema):
    user = await UserService.get_user_or_none(email=register_data.email)
    if user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Пользователь с таким Email уже зарегистрирован.",
        )
    hashed_password = UserService.hash_password(password=register_data.password)
    await UserService.register_user(
        username=register_data.username,
        email=register_data.email,
        hashed_password=hashed_password,
    )
    return status.HTTP_200_OK

@user_router.post("/login")
async def login_user(
    user: UserLoginSchema = Depends(UserService.validation_authentificate_user),
):
    access_token = UserService.create_access_token(user)
    refresh_token = UserService.create_refresh_token(user)
    return UserTokenInfoSchema(
        access_token=access_token,
        refresh_token=refresh_token,
    )