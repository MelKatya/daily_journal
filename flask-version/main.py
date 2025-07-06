from flask import Flask
from core.models import create_tasks_table, create_users_table
from api import app_user


app = Flask(__name__)
app.register_blueprint(app_user)

with app.app_context():
    create_users_table()
    create_tasks_table()


@app.route("/")
def home_page():
    return "home"


if __name__ == "__main__":
    app.run(debug=True)
