from pydantic import BaseModel
from wtforms import Form, StringField, validators


class TaskCreate(BaseModel):
    """
    Валидирует входные данные при создании задачи
    """

    id_users: int
    name: str
    describe: str


class CreateTaskForm(Form):
    """
    WTForms-форма для создания задачи (валидация в веб-форме).
    """

    name = StringField("Название", [validators.Length(min=4, max=25)])
    describe = StringField("Описание", [validators.Length(min=4, max=250)])


class ChangeTaskForm(Form):
    """
    WTForms-форма для изменения задачи (обязательное поле describe).
    """

    describe = StringField(
        "Описание",
        [
            validators.Length(min=4, max=250),
            validators.DataRequired(),
        ],
    )
