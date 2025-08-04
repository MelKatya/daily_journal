from wtforms import Form, PasswordField, StringField, validators


class RegistrationForm(Form):
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
    name = StringField("Имя", [validators.Length(min=4, max=25)])
    password = PasswordField("Пароль")
