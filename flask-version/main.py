import datetime

from flask import Flask, render_template, redirect, url_for

from core.config import settings
from core.models import create_tasks_table, create_users_table
from api import app_route


app = Flask(__name__)
app.register_blueprint(app_route)
app.permanent_session_lifetime = datetime.timedelta(days=7)
app.secret_key = settings.secret_key
# app.config['PERMANENT_SESSION_LIFETIME'] = datetime.timedelta(days=7)

with app.app_context():
    create_users_table()
    create_tasks_table()


@app.route("/")
def home_page():
    return redirect(url_for('app.user.login_user'))


if __name__ == "__main__":
    app.run(debug=True)
