from flask import Blueprint, request, flash, redirect, url_for, render_template, session

from api.utils import check_user_login
from core.schemas.user import RegistrationForm, LoginForm

from crud.user import add_new_user, check_user_exists

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


@app_route.route("/login", methods=["GET", "POST"])
def login_user():
    """Аутентифицирует пользователя"""

    if session.get('user_id') is not None:
        return redirect(url_for("app.user.user_page"))

    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        name, password = form.name.data, form.password.data
        if user_id := check_user_exists(name, password):
            session['user_id'] = user_id
            session['name'] = name
            return redirect(url_for("app.user.user_page"))
        else:
            return "Wrong name or password"
    return render_template("login.html", form=form)


@app_route.route("/logout")
@check_user_login
def logout_user():
    """Удаляет пользователя из сеанса"""
    name = session.get('name')
    session.pop('user_id')
    session.pop('name')
    return f"Bye {name}"


@app_route.route("/users/home")
@check_user_login
def user_page():
    """Загружает домашнюю страницу пользователя"""
    name = session.get('name')
    return render_template("user_page.html", name=name)
