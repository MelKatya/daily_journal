from pydantic import BaseModel, EmailStr
from wtforms import Form, PasswordField, StringField, validators


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


class RegistrationForm(Form):
    """
    Валидирует данные формы регистрации нового пользователя.
    """

    name = StringField("Имя", [validators.Length(min=4, max=25)])
    email = StringField("Email", [validators.Length(min=6, max=35)])
    password = PasswordField(
        "Пароль",
        [
            validators.DataRequired(),
            validators.EqualTo("confirm", message="Пароли не совпадают"),
        ],
    )
    confirm = PasswordField("Повтор пароля")


class LoginForm(Form):
    """
    Валидирует данные формы авторизации пользователя.
    """

    name = StringField("Имя", [validators.Length(min=4, max=25)])
    password = PasswordField("Пароль")