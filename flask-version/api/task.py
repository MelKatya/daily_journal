from flask import Blueprint, request, flash, redirect, url_for, render_template, session
from core.schemas.task import CreateTaskForm

from crud.task import create_task

app_route = Blueprint("task", __name__)


@app_route.route("/tasks", methods=["GET", "POST"])
def create_task_route():
    """Создает новую задачу"""
    if user_id := session.get("user_id"):

        form = CreateTaskForm(request.form)
        if request.method == "POST" and form.validate():
            name, describe = form.name.data, form.describe.data
            create_task(user_id, name, describe)
            return f"{name}, {describe}"
        return render_template("create_task.html", form=form)

    else:
        return "You not login"
