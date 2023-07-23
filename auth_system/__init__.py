from flask import Flask
from flask_login import LoginManager

from auth import auth as auth_blueprint
from main import main as main_blueprint
from models import User

app = Flask(__name__)
login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    return User(user_id)


if __name__ == "__main__":
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(main_blueprint)
    app.run(debug=True)
