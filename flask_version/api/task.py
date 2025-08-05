from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    session,
    url_for,
)
from werkzeug import Response

from api.utils import check_user_login
from core.config import settings
from core.schemas.task import ChangeTaskForm, CreateTaskForm
from crud import task as tsk

app_route = Blueprint("task", __name__)


@app_route.route("/tasks/create", methods=["GET", "POST"])
@check_user_login
def create_task_route() -> Response | str:
    """
    Создает новую задачу.

    Для GET-запроса отображает страницу с формой создания задачи.
    Для POST-запроса обрабатывает данные формы:
        - Проверяет валидность введенных данных.
        - Добавляет новую задачу в бд.
        - Перенаправляет на страницу со всем задачами пользователя.

    Returns:
        Response: редирект на страницу со всем задачами пользователя (POST).
        str: HTML-страница с формой создания новой задачи (GET).
    """
    user_id = session.get(settings.users_data.user_id)
    assert isinstance(user_id, int)

    form = CreateTaskForm(request.form)
    if request.method == "POST" and form.validate():
        name, describe = str(form.name.data), str(form.describe.data)
        tsk.create_task(
            user_id,
            name,
            describe,
        )
        return redirect(url_for("app.task.show_all_tasks"))

    return render_template(
        "create_task.html",
        form=form,
    )


@app_route.route("/tasks", methods=["GET", "POST"])
@check_user_login
def show_all_tasks() -> str:
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

    Returns:
        str: HTML-страница с задачами пользователя.
    """
    #  Получаем параметр сортировки из URL (например, "up" или "down")
    sort_option = request.args.get(
        settings.tasks.SORTED.name, settings.tasks.SORTED.default_html
    )
    assert isinstance(sort_option, str)
    #  Подставляем соответствующее SQL-значение (например, "created_at DESC")
    assert isinstance(settings.tasks.SORTED.db_map, dict)
    sorted_for_db = settings.tasks.SORTED.db_map.get(
        sort_option, settings.tasks.SORTED.default_db
    )

    #  Получаем параметр фильтрации завершенности (например, "completed")
    filter_option = request.args.get(
        settings.tasks.FILTER.name, settings.tasks.FILTER.default_html
    )
    assert isinstance(filter_option, str)
    #  Подставляем соответствующее значение для фильтрации в БД (например, ("true",))
    assert isinstance(settings.tasks.FILTER.db_map, dict)
    filter_for_db = settings.tasks.FILTER.db_map.get(
        filter_option, settings.tasks.FILTER.default_db
    )
    assert isinstance(filter_for_db, tuple)

    #  Получаем строку для поиска по названию задачи
    search_query = request.args.get(
        settings.tasks.SEARCH.name, settings.tasks.SEARCH.default_db
    )
    assert isinstance(search_query, str)

    user_id = session.get(settings.users_data.user_id)
    assert isinstance(user_id, int)
    # Получаем задачи с учетом всех параметров
    tasks = tsk.get_all_tasks(
        user_id=user_id,
        sorted_for_db=sorted_for_db,
        completed=filter_for_db,
        search_query=search_query,
    )

    return render_template(
        "tasks.html",
        tasks=tasks,
        html_param=settings.tasks,
        sort_option=sort_option,
        filter_option=filter_option,
        search_query=search_query,
    )


@app_route.route("/tasks/<int:task_id>", methods=["GET", "POST"])
@check_user_login
def show_task_by_id(task_id: int) -> str:
    """
    Отображает страницу задачу по ID. Также обрабатывает редактирование задачи.

    Для GET-запроса отображает страницу с формой задачи.
    Для POST-запроса обрабатывает данные формы:
    - Если нажата кнопка "Изменить задачу", активируется режим редактирования.
    - Если нажата кнопка "Сохранить изменения", обновляются описание и
        статус выполнения:
        - describe (str): новое описание задачи (через форму).
        - completed (str): статус выполнения ('True' или 'False').

    Если задача с указанным ID не найдена, возвращает страницу ошибки.

    Args:
        task_id (int): ID задачи, которую требуется отобразить или изменить.

    Returns:
        str: HTML-страница с задачей или с сообщением об ошибке (404).
    """
    user_id = session.get(settings.users_data.user_id)
    assert isinstance(user_id, int)

    task = tsk.get_task_by_id(
        user_id=user_id,
        task_id=task_id,
    )
    if task is None:
        return render_template(
            "mistakes.html",
            code=404,
            message=f"Task with id={task_id} not found",
        )

    form = ChangeTaskForm(request.form)
    edit_mode = False

    if request.method == "POST":
        if "change" in request.form:
            edit_mode = True

        elif "save" in request.form and form.validate():
            edit_mode = False
            describe = form.describe.data
            completed = request.form.get("completed")

            if completed == "True":
                tsk.complete_task_by_id(
                    user_id=user_id,
                    task_id=task_id,
                )
            else:
                tsk.not_completed_task_by_id(
                    user_id=user_id,
                    task_id=task_id,
                )

            tsk.change_describe_task_by_id(
                user_id=user_id,
                task_id=task_id,
                describe=describe,
            )

            task = tsk.get_task_by_id(
                user_id=user_id,
                task_id=task_id,
            )

    return render_template(
        "task_id.html",
        task=task,
        edit_mode=edit_mode,
        form=form,
    )


@app_route.route("/tasks/<int:task_id>/before_delete")
@check_user_login
def before_delete_task_by_id(task_id: int) -> str:
    """
    Отображает страницу с запросом на удаление задачи по ее ID.
    Сохраняет флаг подтверждения удаления в сессии.

    Если задача с указанным ID не найдена, возвращает страницу ошибки.

    Args:
        task_id (int): ID задачи, которую требуется удалить.

    Returns:
        str: HTML-страница с запросом или с сообщением об ошибке.
    """
    user_id = session.get(settings.users_data.user_id)
    assert isinstance(user_id, int)

    task = tsk.get_task_by_id(
        user_id=user_id,
        task_id=task_id,
    )
    if not task:
        return render_template(
            "mistakes.html",
            code=404,
            message=f"Task with id={task_id} not found",
        )

    session[f"allow_delete_{task_id}"] = True

    return render_template(
        "delete_id.html",
        task=task,
    )


@app_route.route("/tasks/<int:task_id>/delete")
@check_user_login
def delete_task_by_id(task_id: int) -> Response | str:
    """
    Удаляет задачу по ее ID, если предварительно было подтверждено удаление.

    Проверяет наличие флага подтверждения в сессии. Если флаг не найден,
    возвращает страницу ошибки (403). После удаления флаг удаляется из сессии.

    Args:
        task_id (int): ID задачи, которую требуется удалить.

    Returns:
        Response: редирект на страницу со всем задачами пользователя.
        str: HTML-страница с сообщением об ошибке.
    """
    if not session.pop(f"allow_delete_{task_id}", False):
        return render_template(
            "mistakes.html",
            code=403,
            message="Deletion not confirmed",
        )

    user_id = session.get(settings.users_data.user_id)
    assert isinstance(user_id, int)

    tsk.delete_task_by_id(
        user_id=user_id,
        task_id=task_id,
    )
    return redirect(url_for("app.task.show_all_tasks"))


@app_route.route("/tasks/<int:task_id>/cancel_delete")
@check_user_login
def cancel_delete_task_by_id(task_id: int) -> Response | str:
    """
    Отменяет удаление задачи по ее ID.

    Проверяет наличие флага подтверждения в сессии. Если флаг не найден,
    возвращает страницу ошибки (403). При наличии флага удаляет его из сессии.

    Args:
        task_id (int): ID задачи, удаление которой нужно отменить.

    Returns:
        Response: редирект на страницу задачи, если отмена успешна.
        str: HTML-страница с сообщением об ошибке, если подтверждение
            отсутствует.
    """
    if not session.pop(f"allow_delete_{task_id}", False):
        return render_template(
            "mistakes.html",
            code=403,
            message="Deletion not confirmed",
        )

    return redirect(
        url_for("app.task.show_task_by_id", task_id=task_id),
    )
