from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Response, status, Request, Cookie
from fastapi.params import Query
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from api.utils import check_auth
from core.config import settings
from core.models import db_helper
from core.schemas.tasks import TaskGetForm, TaskCreate, TaskGet, CreateTaskForm, ChangeTaskForm
from crud.task import create_task, get_all_tasks, get_task_by_id, change_describe_task_by_id, not_completed_task_by_id, complete_task_by_id, delete_task_by_id

router = APIRouter(tags=["Tasks"], prefix="/tasks")
templates = Jinja2Templates(directory="templates")


@router.get("/create", response_class=HTMLResponse)
async def show_create_task_form(
    request: Request,
    user=Depends(check_auth),
):
    """Создает новую задачу"""
    form = CreateTaskForm()
    return templates.TemplateResponse(
        name="create_task.html", context={"request": request, "form": form}
    )


@router.post("/create", response_class=HTMLResponse)
async def process_create_task(
    request: Request,
    session: AsyncSession = Depends(db_helper.session_getter),
    user=Depends(check_auth),
):
    """Создает новую задачу"""
    form_data = await request.form()
    form = CreateTaskForm(form_data)

    if form.validate():
        name = str(form.name.data)
        describe = str(form.describe.data)

        await create_task(TaskCreate(id_users=user.id, name=name, describe=describe), session)

        response = RedirectResponse("/users/home", status_code=303)

        return response

    else:
        return templates.TemplateResponse(
            "create_task.html", {"request": request, "form": form}
        )


@router.get("/", response_class=HTMLResponse)
async def show_all_tasks(
    request: Request,
    user=Depends(check_auth),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """
    Обрабатывает запрос на просмотр задач пользователя с параметрами
    сортировки, фильтрации и поиска.
    """
    params = request.query_params
    # Получаем параметр сортировки из URL (напр., "up" или "down")
    sort_option = params.get(
        settings.tasks.SORTED.name, settings.tasks.SORTED.default_html
    )
    assert isinstance(sort_option, str)
    #  Подставляем соответствующее SQL-значение (напр., "created_at DESC")
    assert isinstance(settings.tasks.SORTED.db_map, dict)
    sorted_for_db = settings.tasks.SORTED.db_map.get(
        sort_option, settings.tasks.SORTED.default_db
    )
    # assert isinstance(sorted_for_db, str)

    # Получаем параметр фильтрации завершенности (напр., "completed")
    filter_option = params.get(
        settings.tasks.FILTER.name, settings.tasks.FILTER.default_html
    )
    assert isinstance(filter_option, str)
    # Подставляем соответствующее значение для фильтрации в бд (напр., "true")
    assert isinstance(settings.tasks.FILTER.db_map, dict)
    filter_for_db = settings.tasks.FILTER.db_map.get(
        filter_option, settings.tasks.FILTER.default_db
    )
    assert isinstance(filter_for_db, list)

    # Получаем строку для поиска по названию задачи
    search_query = params.get(
        settings.tasks.SEARCH.name, settings.tasks.SEARCH.default_db
    )
    assert isinstance(search_query, str)

    print(sorted_for_db, filter_for_db, search_query)
    # Получаем задачи с учетом всех параметров
    tasks = await get_all_tasks(
        id_users=user.id,
        sorted_for_db=sorted_for_db,
        completed=filter_for_db,
        search_query=search_query,
        session=session,
    )

    return templates.TemplateResponse(
        "tasks.html",
        {
            "request": request,
            "tasks": tasks,
            "html_param": settings.tasks,
            "sort_option": sort_option,
            "filter_option": filter_option,
            "search_query": search_query,
        }
    )


@router.get("/{task_id}", response_class=HTMLResponse)
async def show_task_id_form(
    task_id: int,
    request: Request,
    user=Depends(check_auth),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Отображает страницу задачу по ID."""
    form = ChangeTaskForm()
    edit_mode = False
    task = await get_task_by_id(id_users=user.id, task_id=task_id, session=session)

    return templates.TemplateResponse(
        name="task_id.html",
        context={
            "request": request,
            "task": task,
            "edit_mode": edit_mode,
            "form": form,
        }
    )


@router.post("/{task_id}", response_class=HTMLResponse)
async def show_task_id_change(
    task_id: int,
    request: Request,
    user=Depends(check_auth),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    """Отображает страницу задачу по ID."""
    form_data = await request.form()
    form = ChangeTaskForm(form_data)
    edit_mode = False
    task = await get_task_by_id(id_users=user.id, task_id=task_id, session=session)

    if "change" in form_data:
        edit_mode = True

    elif "save" in form_data and form.validate():
        edit_mode = False
        describe = form.describe.data
        assert isinstance(describe, str)

        completed = form_data.get("completed")

        if completed == "True":
            await complete_task_by_id(
                id_users=user.id,
                task_id=task_id,
                session=session,
            )

        else:
            await not_completed_task_by_id(
                id_users=user.id,
                task_id=task_id,
                session=session,
            )

        await change_describe_task_by_id(
            id_users=user.id,
            task_id=task_id,
            describe=describe,
            session=session,
        )

        task = await get_task_by_id(id_users=user.id, task_id=task_id, session=session)

    return templates.TemplateResponse(
        name="task_id.html",
        context={
            "request": request,
            "task": task,
            "edit_mode": edit_mode,
            "form": form,
        }
    )


@router.get("/{task_id}/before_delete", response_class=HTMLResponse)
async def before_delete_task_by_id(
    task_id: int,
    request: Request,
    response: Response,
    user=Depends(check_auth),
    session: AsyncSession = Depends(db_helper.session_getter),
):
    task = await get_task_by_id(id_users=user.id, task_id=task_id, session=session)

    template_response = templates.TemplateResponse(
        name="delete_id.html",
        context={
            "request": request,
            "task": task,
        }
    )
    template_response.set_cookie(key="allow_delete", value=str(task_id), httponly=True)
    return template_response


@router.get("/{task_id}/delete", response_class=HTMLResponse)
async def delete_task_by_id_form(
    task_id: int,
    request: Request,
    allow_delete=Cookie(default=None),
    user=Depends(check_auth),
    session: AsyncSession = Depends(db_helper.session_getter),
):

    if allow_delete != str(task_id):
        template_response = templates.TemplateResponse(
            name="mistakes.html",
            context={
                "request": request,
                "code": 403,
                "message": "Deletion not confirmed"
            }
        )
        template_response.delete_cookie(key="allow_delete", httponly=True)
        return template_response

    await delete_task_by_id(
        id_users=user.id,
        task_id=task_id,
        session=session,
    )

    response = RedirectResponse("/tasks/")
    response.delete_cookie(key="allow_delete", httponly=True)

    return response


@router.get("/{task_id}/cancel_delete", response_class=HTMLResponse)
async def cancel_delete_task_by_id(
    task_id: int,
    request: Request,
    allow_delete=Cookie(default=None),
    user=Depends(check_auth),
):

    if allow_delete != str(task_id):
        template_response = templates.TemplateResponse(
            name="mistakes.html",
            context={
                "request": request,
                "code": 403,
                "message": "Deletion not confirmed"
            }
        )
        template_response.delete_cookie(key="allow_delete", httponly=True)
        return template_response

    response = RedirectResponse(f"/tasks/{task_id}")
    response.delete_cookie(key="allow_delete", httponly=True)

    return response
