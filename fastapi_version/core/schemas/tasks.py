from pydantic import BaseModel


class TaskBase(BaseModel):
    id_users: int


class TaskGetForm(BaseModel):
    name: str
    describe: str


class TaskCreate(TaskBase, TaskGetForm):
    pass

