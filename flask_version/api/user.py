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
from core.schemas.user import LoginForm, RegistrationForm
from crud.user import add_new_user, check_user_exists

app_route = Blueprint("user", __name__)


@app_route.route("/registration", methods=["GET", "POST"])
def registers_new_user():
    """Создает нового пользователя"""
    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate():
        name, email, password = (
            form.name.data,
            form.email.data,
            form.password.data,
        )  # noqa E501
        add_new_user(name, email, password)
        return f"{name}, {email}, {password}"
    return render_template("register.html", form=form)


@app_route.route("/login", methods=["GET", "POST"])
def login_user():
    """Аутентифицирует пользователя"""

    if session.get("user_id") is not None:
        return redirect(url_for("app.user.user_page"))

    form = LoginForm(request.form)
    if request.method == "POST" and form.validate():
        name, password = form.name.data, form.password.data
        if user_id := check_user_exists(name, password):
            session[settings.users_data.user_id] = user_id
            session[settings.users_data.name] = name
            return redirect(url_for("app.user.user_page"))
        else:
            return render_template(
                "mistakes.html", code=403, message="Wrong name or password"
            )
    return render_template("login.html", form=form)


@app_route.route("/logout")
@check_user_login
def logout_user():
    """Удаляет пользователя из сеанса"""
    session.get(settings.users_data.name)
    session.pop(settings.users_data.user_id)
    session.pop(settings.users_data.name)
    return redirect(url_for("app.user.login_user"))


@app_route.route("/users/home")
@check_user_login
def user_page():
    """Загружает домашнюю страницу пользователя"""
    name = session.get(settings.users_data.name)
    return render_template("user_page.html", name=name)
