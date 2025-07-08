from flask import Blueprint, request, flash, redirect, url_for, render_template, session

from functools import wraps


def check_user_login(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if session.get("user_id"):
            resul_func = func(*args, **kwargs)
            return resul_func
        else:
            return "You aren't login"

    return wrapper
