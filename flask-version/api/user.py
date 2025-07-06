from flask import Blueprint, request, flash, redirect, url_for, render_template, session
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
    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        name, password = form.name.data, form.password.data
        if user_id := check_user_exists(name, password):
            session['user_id'] = user_id
            session['name'] = name
            return f"welcome {name}"
        else:
            return "Wrong name or password"
    return render_template("login.html", form=form)


@app_route.route("/logout")
def logout_user():
    """Удаляет пользователя из сеанса"""
    if "user_id" in session:
        session.pop('user_id')
        name = session.get('name')
        session.pop('name')
        return f"Bye {name}"
    else:
        return "Wrong name or password"

