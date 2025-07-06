from flask import Blueprint, request, flash, redirect, url_for, render_template
from core.schemas.user import RegistrationForm

from crud.user import add_new_user

app_route = Blueprint("user", __name__)


@app_route.route("/registration", methods=["GET", "POST"])
def registers_new_user():
    """Создает нового пользователя"""
    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate():
        name, email, password = form.name.data, form.email.data, form.password.data
        add_new_user(name, email, password)
        return f"{name}, {email}, {password}"
    return render_template("register.html", form=form)
