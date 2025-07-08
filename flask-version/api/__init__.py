from flask import Blueprint

from .user import app_route as app_user

app_route = Blueprint("app", __name__)
app_route.register_blueprint(app_user)
