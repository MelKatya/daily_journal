from wtforms import Form, StringField, IntegerField, validators, PasswordField, BooleanField


class CreateTaskForm(Form):
    name = StringField("Название", [validators.Length(min=4, max=25)])
    describe = StringField("Описание", [validators.Length(min=4, max=250)])


class ChangeTaskForm(Form):
    describe = StringField("Описание", [validators.Length(min=4, max=250)])
