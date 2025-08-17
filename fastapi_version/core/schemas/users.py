from pydantic import BaseModel, EmailStr
from wtforms import Form, PasswordField, StringField, validators


class UserCreate(BaseModel):
    """
    Валидирует входные данные при создании пользователя
    """

    name: str
    hashed_password: str
    email: EmailStr


class RegistrationForm(Form):
    """
    WTForms-форма регистрации (проверка имени, email, пароля + подтверждение).
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
    WTForms-форма входа (валидация имени и пароля).
    """

    name = StringField("Имя", [validators.Length(min=4, max=25)])
    password = PasswordField("Пароль")
