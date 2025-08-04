from flask import Blueprint

from .task import app_route as app_task
from .user import app_route as app_user

app_route = Blueprint("app", __name__)
app_route.register_blueprint(app_user)
app_route.register_blueprint(app_task)
