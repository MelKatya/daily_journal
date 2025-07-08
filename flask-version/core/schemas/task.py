from wtforms import Form, StringField, IntegerField, validators, PasswordField


class CreateTaskForm(Form):
    name = StringField("Name", [validators.Length(min=4, max=25)])
    describe = StringField("Describe", [validators.Length(min=4, max=250)])
