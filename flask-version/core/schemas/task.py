from wtforms import Form, StringField, IntegerField, validators, PasswordField


class CreateTaskForm(Form):
    name = StringField("Название", [validators.Length(min=4, max=25)])
    describe = StringField("Описание", [validators.Length(min=4, max=250)])
