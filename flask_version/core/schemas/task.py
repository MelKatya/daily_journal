from wtforms import Form, StringField, validators


class CreateTaskForm(Form):
    """
    Валидирует данные формы создания задачи.
    """

    name = StringField("Название", [validators.Length(min=4, max=25)])
    describe = StringField("Описание", [validators.Length(min=4, max=250)])


class ChangeTaskForm(Form):
    """
    Валидирует данные формы изменения задачи.
    """

    describe = StringField(
        "Описание",
        [
            validators.Length(min=4, max=250),
            validators.DataRequired(),
        ],
    )
