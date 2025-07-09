from flask import Blueprint, request, flash, redirect, url_for, render_template, session, jsonify

from api.utils import check_user_login
from core.schemas.task import CreateTaskForm

from crud import task as tsk

app_route = Blueprint("task", __name__)


@app_route.route("/tasks/create", methods=["GET", "POST"])
@check_user_login
def create_task_route():
    """Создает новую задачу"""
    form = CreateTaskForm(request.form)
    if request.method == "POST" and form.validate():
        name, describe = form.name.data, form.describe.data
        tsk.create_task(session.get("user_id"), name, describe)
        return f"{name}, {describe}"
    return render_template("create_task.html", form=form)


@app_route.route("/tasks", methods=["GET"])
@check_user_login
def show_all_tasks():
    """Выводит все задачи текущего пользователя"""
    tasks = tsk.get_all_tasks(user_id=session.get("user_id"))
    return tasks


@app_route.route("/tasks/<int:task_id>", methods=["GET"])
@check_user_login
def show_task_by_id(task_id: int):
    """Выводит информацию о задаче по id"""
    task = tsk.get_task_by_id(user_id=session.get("user_id"), task_id=task_id)
    if not task:
        return jsonify(message=f"Task with id={task_id} not found"), 404
    return task


@app_route.route("/tasks/<int:task_id>/complete", methods=["GET"])
@check_user_login
def complete_task_by_id(task_id: int):
    """Помечает задачу выполненной"""
    task = tsk.get_task_by_id(user_id=session.get("user_id"), task_id=task_id)
    if not task:
        return jsonify(message=f"Task with id={task_id} not found"), 404

    task = tsk.complete_task_by_id(user_id=session.get("user_id"), task_id=task_id)
    if not task:
        return jsonify(message=f"Task with id={task_id} already completed")
    return task

