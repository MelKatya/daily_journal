from functools import wraps

from core.config import settings
from flask import redirect, session, url_for


def check_user_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get(settings.users_data.user_id):
            return func(*args, **kwargs)
        else:
            return redirect(url_for("app.user.login_user"))

    return wrapper
