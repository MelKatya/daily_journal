from pydantic import BaseModel
from sqlalchemy.orm import Query
from wtforms import Form, StringField, validators


class TaskBase(BaseModel):
    id_users: int


class TaskGetForm(BaseModel):
    name: str
    describe: str


class TaskCreate(TaskBase, TaskGetForm):
    pass


class TaskGet(TaskBase):
    sort_option: str = "up"
    filter_option: str = "all"
    search_query: str = ""


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