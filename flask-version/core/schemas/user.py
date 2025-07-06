from wtforms import Form, StringField, IntegerField, validators, PasswordField


class RegistrationForm(Form):
    name = StringField("name", [validators.Length(min=4, max=25)])
    email = StringField("Email Address", [validators.Length(min=6, max=35)])
    password = PasswordField(
        "New Password",
        [
            validators.DataRequired(),
            validators.EqualTo("confirm", message="Passwords must match"),
        ],
    )
    confirm = PasswordField("Repeat Password")
