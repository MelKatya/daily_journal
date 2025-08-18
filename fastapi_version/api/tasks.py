from api.utils import check_auth
from core.config import settings
from core.models import Task, User, db_helper
from core.schemas.tasks import ChangeTaskForm, CreateTaskForm, TaskCreate
from crud import task as tsk
from fastapi import APIRouter, Cookie, Depends, HTTPException, Request, status
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(tags=["Tasks"], prefix="/tasks")
templates = settings.templates


@router.get("/create", response_class=HTMLResponse)
async def show_create_task_form(
    request: Request,
    user: User = Depends(check_auth),  # noqa B008
) -> HTMLResponse:
    """
    Обрабатывает GET-запрос с формой создания новой задачи.

    Args:
        request (Request): объект запроса FastAPI.
        user (User): объект текущего пользователя.

    Returns:
        HTMLResponse: отрендеренный шаблон "create_task.html"
            с формой для создания задачи.
    """
    form = CreateTaskForm()
    return templates.TemplateResponse(
        name="create_task.html", context={"request": request, "form": form}
    )


@router.post("/create", response_class=HTMLResponse)
async def process_create_task(
    request: Request,
    session: AsyncSession = Depends(db_helper.session_getter),  # noqa B008
    user: User = Depends(check_auth),  # noqa B008
) -> HTMLResponse | RedirectResponse:
    """
    Обрабатывает POST-запрос на создание новой задачи.
    - Проверяет валидность введенных данных.
    - Добавляет новую задачу в бд.
    - Перенаправляет на страницу со всеми задачами пользователя.

    Args:
        request (Request): объект запроса FastAPI.
        session (AsyncSession): асинхронная сессия SQLAlchemy.
        user (User): объект текущего пользователя.

    Returns:
        HTMLResponse | RedirectResponse:
            - RedirectResponse — редирект на страницу со всем задачами
                пользователя.
            - HTMLResponse — форма создания задачи с ошибкой.
    """
    form_data = await request.form()
    form = CreateTaskForm(form_data)

    if form.validate():
        name = str(form.name.data)
        describe = str(form.describe.data)

        await tsk.create_task(
            TaskCreate(id_users=user.id, name=name, describe=describe), session
        )

        return RedirectResponse("/tasks", status_code=303)

    else:
        return templates.TemplateResponse(
            "create_task.html", {"request": request, "form": form}
        )


@router.get("", response_class=HTMLResponse)
async def show_all_tasks(
    request: Request,
    user: User = Depends(check_auth),  # noqa B008
    session: AsyncSession = Depends(db_helper.session_getter),  # noqa B008
) -> HTMLResponse:
    """
    Обрабатывает запрос на просмотр задач пользователя с параметрами
    сортировки, фильтрации и поиска.

    Получает значения из URL-параметров:
    - sorted: порядок сортировки ('up', 'down', 'name', 'completed').
    - filter: фильтрация по статусу выполнения
        ('all', 'completed', 'uncompleted').
    - search: поисковый запрос по названию задачи.

    В зависимости от выбранных значений подставляет соответствующие
    SQL-параметры и возвращает HTML-страницу с отфильтрованными задачами.

    Args:
        request (Request): объект запроса FastAPI.
        user (User): объект текущего пользователя.
        session (AsyncSession): асинхронная сессия SQLAlchemy.

    Returns:
        HTMLResponse: страница с задачами пользователя.
    """
    params = request.query_params

    # Получаем параметр сортировки из URL (напр., "up" или "down")
    sort_option = params.get(
        settings.tasks.SORTED.name, settings.tasks.SORTED.default_html
    )
    assert isinstance(sort_option, str)
    #  Подставляем соответствующее SQL-значение (напр., "created_at")
    assert isinstance(settings.tasks.SORTED.db_map, dict)
    sorted_for_db = settings.tasks.SORTED.db_map.get(
        sort_option, settings.tasks.SORTED.default_db
    )

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

    # Получаем задачи с учетом всех параметров
    tasks = await tsk.get_all_tasks(
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
        },
    )


@router.get("/{task_id}", response_class=HTMLResponse)
async def show_task_id_form(
    task_id: int,
    request: Request,
    user: User = Depends(check_auth),  # noqa B008
    session: AsyncSession = Depends(db_helper.session_getter),  # noqa B008
) -> HTMLResponse:
    """
    Отображает страницу задачу по ID.

    Args:
        task_id (int): ID задачи.
        request (Request): объект запроса FastAPI.
        user (User): объект текущего пользователя.
        session (AsyncSession): асинхронная сессия SQLAlchemy.

    Returns:
        HTMLResponse: страница с задачами пользователя.
    """
    form = ChangeTaskForm()
    edit_mode = False
    task = await tsk.get_task_by_id(
        id_users=user.id,
        task_id=task_id,
        session=session,
    )

    return templates.TemplateResponse(
        name="task_id.html",
        context={
            "request": request,
            "task": task,
            "edit_mode": edit_mode,
            "form": form,
        },
    )


@router.post("/{task_id}", response_class=HTMLResponse)
async def show_task_id_change(
    task_id: int,
    request: Request,
    user: User = Depends(check_auth),  # noqa B008
    session: AsyncSession = Depends(db_helper.session_getter),  # noqa B008
) -> HTMLResponse:
    """
    Обрабатывает данные формы для задачи.
    - Если нажата кнопка "Изменить задачу", активируется режим редактирования.
    - Если нажата кнопка "Сохранить изменения", обновляются описание и
        статус выполнения:
        - describe (str): новое описание задачи (через форму).
        - completed (str): статус выполнения ('True' или 'False').

    Args:
        task_id (int): ID задачи.
        request (Request): объект запроса FastAPI.
        user (User): объект текущего пользователя.
        session (AsyncSession): асинхронная сессия SQLAlchemy.

    Returns:
        HTMLResponse: HTML-страница с задачей (в режиме просмотра
            или редактирования).
    """
    form_data = await request.form()
    form = ChangeTaskForm(form_data)
    edit_mode = False

    task = await tsk.get_task_by_id(
        id_users=user.id,
        task_id=task_id,
        session=session,
    )
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id={task_id} not found",
        )

    if "change" in form_data:
        edit_mode = True

    elif "save" in form_data and form.validate():
        edit_mode = False
        describe = form.describe.data
        assert isinstance(describe, str)

        completed = form_data.get("completed")

        if completed == "True":
            await tsk.complete_task_by_id(
                id_users=user.id,
                task_id=task_id,
                session=session,
            )

        else:
            await tsk.not_completed_task_by_id(
                id_users=user.id,
                task_id=task_id,
                session=session,
            )

        await tsk.change_describe_task_by_id(
            id_users=user.id,
            task_id=task_id,
            describe=describe,
            session=session,
        )

        task: Task | None = await tsk.get_task_by_id(  # type: ignore[no-redef]
            id_users=user.id, task_id=task_id, session=session
        )

    return templates.TemplateResponse(
        name="task_id.html",
        context={
            "request": request,
            "task": task,
            "edit_mode": edit_mode,
            "form": form,
        },
    )


@router.get("/{task_id}/before_delete", response_class=HTMLResponse)
async def before_delete_task_by_id(
    task_id: int,
    request: Request,
    user: User = Depends(check_auth),  # noqa B008
    session: AsyncSession = Depends(db_helper.session_getter),  # noqa B008
) -> HTMLResponse:
    """
    Отображает страницу с подтверждением удаления задачи по ееID.
    Если задача существует, устанавливает Cookie 'allow_delete' с ее ID.
    Если задача не найдена, возвращает страницу ошибки (404).

    Args:
        task_id (int): ID задачи.
        request (Request): объект запроса FastAPI.
        user (User): объект текущего пользователя.
        session (AsyncSession): асинхронная сессия SQLAlchemy.

    Returns:
        HTMLResponse:
            - страница подтверждения удаления с установленным Cookie.
            - страница ошибки, если задача не найдена.
    """
    task = await tsk.get_task_by_id(
        id_users=user.id,
        task_id=task_id,
        session=session,
    )
    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Task with id={task_id} not found",
        )

    template_response = templates.TemplateResponse(
        name="delete_id.html",
        context={
            "request": request,
            "task": task,
        },
    )
    template_response.set_cookie(
        key="allow_delete",
        value=str(task_id),
        httponly=True,
    )
    return template_response


@router.get("/{task_id}/delete", response_class=HTMLResponse)
async def delete_task_by_id_form(
    task_id: int,
    request: Request,
    allow_delete: str | None = Cookie(default=None),  # noqa B008
    user: User = Depends(check_auth),  # noqa B008
    session: AsyncSession = Depends(db_helper.session_getter),  # noqa B008
) -> HTMLResponse | RedirectResponse:
    """
    Удаляет задачу по ее ID, если предварительно было подтверждено удаление.

    Для подтверждения используется Cookie 'allow_delete', значение которого
    должно совпадать с ID задачи. Если Cookie отсутствует или не совпадает,
    возвращается страница ошибки (403). После выполнения операции
    (успешной или нет) Cookie 'allow_delete' удаляется.

    Args:
        task_id (int): ID задачи.
        request (Request): объект запроса FastAPI.
        allow_delete (str | None): Cookie, подтверждающий удаление задачи.
        user (User): объект текущего пользователя.
        session (AsyncSession): асинхронная сессия SQLAlchemy.

    Returns:
        HTMLResponse | RedirectResponse:
            - RedirectResponse — редирект на страницу со всем задачами.
            - HTMLResponse — страница ошибки, если удаление не подтверждено.
    """
    if allow_delete != str(task_id):
        template_response = templates.TemplateResponse(
            name="mistakes.html",
            context={
                "request": request,
                "code": 403,
                "message": "Deletion not confirmed",
            },
        )
        template_response.delete_cookie(key="allow_delete", httponly=True)
        return template_response

    await tsk.delete_task_by_id(
        id_users=user.id,
        task_id=task_id,
        session=session,
    )

    response = RedirectResponse("/tasks")
    response.delete_cookie(key="allow_delete", httponly=True)

    return response


@router.get("/{task_id}/cancel_delete", response_class=HTMLResponse)
async def cancel_delete_task_by_id(
    task_id: int,
    request: Request,
    allow_delete: str | None = Cookie(default=None),  # noqa B008
    user: User = Depends(check_auth),  # noqa B008
) -> HTMLResponse | RedirectResponse:
    """
    Отменяет удаление задачи по ее ID.

    Для отмены используется Cookie 'allow_delete', значение которого должно
    совпадать с ID задачи. Если Cookie отсутствует или не совпадает,
    возвращается страница ошибки (403). После выполнения операции
    Cookie 'allow_delete' удаляется.

    Args:
        task_id (int): ID задачи.
        request (Request): объект запроса FastAPI.
        allow_delete (str | None):  Cookie, подтверждающий удаление задачи.
        user (User): объект текущего пользователя.

    Returns:
        HTMLResponse | RedirectResponse:
            - RedirectResponse — перенаправление на страницу задачи после
                успешной отмены.
            - HTMLResponse — страница ошибки, если удаление не подтверждено.
    """
    if allow_delete != str(task_id):
        template_response = templates.TemplateResponse(
            name="mistakes.html",
            context={
                "request": request,
                "code": 403,
                "message": "Deletion not confirmed",
            },
        )
        template_response.delete_cookie(key="allow_delete", httponly=True)
        return template_response

    response = RedirectResponse(f"/tasks/{task_id}")
    response.delete_cookie(key="allow_delete", httponly=True)

    return response
