from flask import (
    Blueprint,
    redirect,
    render_template,
    request,
    session,
    url_for,
)

from api.utils import check_user_login
from core.config import settings
from core.schemas.task import ChangeTaskForm, CreateTaskForm
from crud import task as tsk

app_route = Blueprint("task", __name__)


@app_route.route("/tasks/create", methods=["GET", "POST"])
@check_user_login
def create_task_route():
    """
    Создает новую задачу
    """
    form = CreateTaskForm(request.form)
    if request.method == "POST" and form.validate():
        name, describe = form.name.data, form.describe.data
        tsk.create_task(
            session.get(settings.users_data.user_id),
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
def show_all_tasks():
    """
    Выводит все задачи текущего пользователя.
    Сортирует, фильтрует их и выполняет поиск
    """
    sort_option = request.args.get(
        settings.tasks.SORTED.name, settings.tasks.SORTED.default_html
    )
    sorted_for_db = settings.tasks.SORTED.db_map.get(
        sort_option, settings.tasks.SORTED.default_db
    )

    filter_option = request.args.get(
        settings.tasks.FILTER.name, settings.tasks.FILTER.default_html
    )
    filter_for_db = settings.tasks.FILTER.db_map.get(
        filter_option, settings.tasks.FILTER.default_db
    )

    search_query = request.args.get(
        settings.tasks.SEARCH.name, settings.tasks.SEARCH.default_db
    )

    tasks = tsk.get_all_tasks(
        user_id=session.get(settings.users_data.user_id),
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
def show_task_by_id(task_id: int):
    """
    Выводит информацию о задаче по id, позволяет ее изменять
    """
    user_id = session.get(settings.users_data.user_id)

    if not user_id:
        return render_template(
            "mistakes.html",
            code=403,
            message="You are not logged in",
        )

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

    return render_template(
        "task_id.html",
        task=task,
        edit_mode=edit_mode,
        form=form,
    )


@app_route.route("/tasks/<int:task_id>/before_delete", methods=["GET", "POST"])
@check_user_login
def before_delete_task_by_id(task_id: int):
    """
    Запрашивает подтверждение пользователя на удаление задачи
    """
    user_id = session.get(settings.users_data.user_id)

    if not user_id:
        return render_template(
            "mistakes.html",
            code=403,
            message="You are not logged in",
        )

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


@app_route.route("/tasks/<int:task_id>/delete", methods=["GET", "POST"])
@check_user_login
def delete_task_by_id(task_id: int):
    """
    Удаляет задачу
    """
    if not session.pop(f"allow_delete_{task_id}", False):
        return render_template(
            "mistakes.html",
            code=403,
            message="Deletion not confirmed",
        )

    user_id = session.get(settings.users_data.user_id)

    if not user_id:
        return render_template(
            "mistakes.html",
            code=403,
            message="You are not logged in",
        )

    tsk.delete_task_by_id(
        user_id=user_id,
        task_id=task_id,
    )
    return redirect(url_for("app.task.show_all_tasks"))


@app_route.route("/tasks/<int:task_id>/cancel_delete", methods=["GET"])
@check_user_login
def cancel_delete_task_by_id(task_id: int):
    """
    Отменяет удаление задачи
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
