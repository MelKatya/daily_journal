from pydantic import BaseModel, EmailStr


class UserBase(BaseModel):
    name: str


class UserLogin(UserBase):
    password: str


class UserCreateRead(UserLogin):
    email: EmailStr


class UserHashPass(UserBase):
    hashed_password: str


class UserCreate(UserHashPass):
    email: EmailStr


