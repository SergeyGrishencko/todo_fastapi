from pydantic import BaseModel, EmailStr

class UserTokenInfoSchema(BaseModel):
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"

class UserRegisterSchema(BaseModel):
    username: str
    email: EmailStr
    password: str

class UserLoginSchema(BaseModel):
    username: str
    password: str