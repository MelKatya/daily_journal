from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: str


class UserLogin(UserBase):
    password: str


class UserCreateRead(UserLogin):
    email: EmailStr


class UserCreate(UserBase):
    email: EmailStr
    hashed_password: str


