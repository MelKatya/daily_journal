from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.utils import check_auth
from core.models import db_helper
from core.schemas.tasks import TaskGetForm, TaskCreate
from crud.task import create_task

router = APIRouter(tags=["Tasks"], prefix="/tasks")


@router.post("/")
async def create_task_route(
    new_task: TaskGetForm,
    user=Depends(check_auth),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    task = await create_task(TaskCreate(id_users=user.id, **new_task.model_dump()), session)
    return task
