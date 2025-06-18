import bcrypt
import jwt

from fastapi import Form, HTTPException, status
from sqlalchemy import select, insert
from datetime import timedelta, datetime, timezone

from models.user import User
from schemas.users import UserLoginSchema
from backend.session import async_session_maker
from backend.config import settings

TOKEN_TYPE_FIELD = "type"
ACCESS_TOKEN_TYPE = "access"
REFRESH_TOKEN_TYPE = "refresh"

def decoded_jwt(
    token: str | bytes,
    key: str = settings.auth_jwt.public_key_path.read_text(),
    algorithm: str = settings.auth_jwt.algorithm,
):
    token_bytes = token.encode()
    decoded = jwt.decode(
        token_bytes, 
        key, 
        algorithms=[algorithm],
    )
    return decoded

class UserService:
    model = User

    @classmethod
    async def register_user(cls, **register_data):
        async with async_session_maker() as session:
            stmt = insert(cls.model).values(**register_data)
            await session.execute(stmt)
            await session.commit()

    @classmethod
    async def get_user_or_none(cls, **user_data):
        async with async_session_maker() as session:
            query = select(cls.model).filter_by(**user_data)
            result = await session.execute(query)
            return result.scalar_one_or_none()
        
    @classmethod
    def hash_password(cls, password: str) -> bytes:
        salt = bcrypt.gensalt()
        password_bytes: bytes = password.encode()
        return bcrypt.hashpw(password_bytes, salt)
    
    @classmethod
    def validate_password(
        cls,
        password: str,
        hashed_password: bytes,
    ) -> bool:
        return bcrypt.checkpw(
            password=password.encode(),
            hashed_password=hashed_password,
        )
    
    
    @classmethod
    async def validation_authentificate_user(
        cls,
        username: str = Form(),
        password: str = Form(),
    ):
        user = await cls.get_user_or_none(username=username)
        unauthed_exception = HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED
        )

        if user is None:
            raise unauthed_exception
        
        if cls.validate_password(
            password=password,
            hashed_password=user.hashed_password,
        ):
            return user
        
        raise unauthed_exception
    
    @classmethod
    def encode_jwt(
        cls,
        payload: dict,
        private_key: str = settings.auth_jwt.private_key_path.read_text(),
        algorithm: str = settings.auth_jwt.algorithm,
        expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
        expire_timedelta: timedelta | None = None,
    ):
        to_encode = payload.copy()
        now = datetime.now(timezone.utc)
        if expire_timedelta:
            expire = now + expire_timedelta
        else:
            expire = now + timedelta(minutes=expire_minutes)
        to_encode.update(
            exp=expire,
            iat=now,
        )
        encoded = jwt.encode(
            to_encode,
            private_key,
            algorithm=algorithm,
        )
        return encoded

    @classmethod
    def create_jwt(
        cls,
        token_type: str, 
        payload: dict,
        expire_minutes: int = settings.auth_jwt.access_token_expire_minutes,
        expire_timedelta: timedelta | None = None,
    ) -> str:
        jwt_payload = {TOKEN_TYPE_FIELD: token_type}
        jwt_payload.update(payload)
        return cls.encode_jwt(
            payload=jwt_payload,
            expire_minutes=expire_minutes,
            expire_timedelta=expire_timedelta,
        )

    @classmethod
    def create_access_token(cls, user: UserLoginSchema) -> str:
        jwt_payload = {
            "id": str(user.id),
            "username": user.username,
        }
        return cls.create_jwt(
            token_type=ACCESS_TOKEN_TYPE, 
            payload=jwt_payload,
            expire_minutes=settings.auth_jwt.access_token_expire_minutes,
        )
    
    @classmethod
    def create_refresh_token(cls, user:UserLoginSchema) -> str:
        jwt_payload = {
            "sub": user.username,
        }
        return cls.create_jwt(
            token_type=REFRESH_TOKEN_TYPE, 
            payload=jwt_payload,
            expire_timedelta=timedelta(settings.auth_jwt.refresh_token_expire_days),
        )