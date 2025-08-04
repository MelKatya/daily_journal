from flask import (
    Blueprint,
    Response,
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
def registers_new_user() -> Response | str:
    """
    Обрабатывает регистрацию нового пользователя.

    Для GET-запроса отображает страницу с формой регистрации.
    Для POST-запроса обрабатывает данные формы:
        - Проверяет валидность введенных данных.
        - Создает нового пользователя с помощью 'add_new_user'.
        - Перенаправляет на страницу авторизации.

    Returns:
        Response: редирект на страницу логина (POST).
        str: HTML-страница с формой регистрации (GET).
    """
    form = RegistrationForm(request.form)
    if request.method == "POST" and form.validate():
        name, email, password = (
            form.name.data,
            form.email.data,
            form.password.data,
        )
        add_new_user(name, email, password)
        return redirect(url_for("app.user.login_user"))

    return render_template("register.html", form=form)


@app_route.route("/login", methods=["GET", "POST"])
def login_user() -> Response | str:
    """
    Обрабатывает авторизацию пользователя.

    Если пользователь уже авторизован (есть user_id в сессиях),
    то выполняет редирект на основную страницу пользователя.

    Для GET-запроса отображает страницу с формой авторизации.
    Для POST-запроса обрабатывает данные формы:
        - Проверяет валидность введенных данных.
        - Перенаправляет на основную страницу пользователя.
        - Если введен неверно логин и/или пароль,
            то перенаправляет на страницу с ошибкой.

    Returns:
        Response: редирект на страницу пользователя (POST).
        str: HTML-страница с формой авторизации (GET)
            или с сообщением об ошибке (неудачный POST)..
    """

    if session.get(settings.users_data.user_id) is not None:
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
def logout_user() -> Response:
    """
    Удаляет данные пользователя из сессии и перенаправляет
    на страницу авторизации.

    Returns:
        Response: редирект на страницу авторизации.
    """
    session.pop(settings.users_data.user_id)
    session.pop(settings.users_data.name)
    return redirect(url_for("app.user.login_user"))


@app_route.route("/users/home")
@check_user_login
def user_page() -> str:
    """
    Загружает основную страницу пользователя.

    Returns:
        str: HTML-страница пользователя.
    """
    name = session.get(settings.users_data.name)
    return render_template("user_page.html", name=name)
