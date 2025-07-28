from flask import session, redirect, url_for

from functools import wraps

from core.config import settings


def check_user_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get(settings.users_data.user_id):
            resul_func = func(*args, **kwargs)
            return resul_func
        else:
            return redirect(url_for("app.user.login_user"))

    return wrapper
