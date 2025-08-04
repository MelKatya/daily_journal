from functools import wraps
from typing import Any, Callable

from flask import redirect, session, url_for

from core.config import settings


def check_user_login(func) -> Callable:
    """
    Декоратор, проверяющий, авторизован ли пользователь перед
    выполнением функции func.

    Если пользователь авторизован (в сессии присутствует ключ с user_id),
    вызывается оригинальная функция. В противном случае происходит
    редирект на страницу логина.

    Args:
        func (Callable): функция, к которой применяется декоратор.

    Returns:
        Callable: обернутая функция, с выполненной проверкой авторизации.
    """

    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        """
        Обертка, проверяющая наличие user_id в сессии перед вызовом функции.

        Args:
            *args: позиционные аргументы, передаваемые в исходную функцию.
            **kwargs: именованные аргументы, передаваемые в исходную функцию.

        Returns:
            Any: результат выполнения исходной функции или редирект
            на страницу логина.
        """
        if session.get(settings.users_data.user_id):
            return func(*args, **kwargs)
        else:
            return redirect(url_for("app.user.login_user"))

    return wrapper
