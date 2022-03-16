from flask import Flask
from flask_login import LoginManager
from .models import UserModel
from .auth import auth

login_manager = LoginManager()
login_manager.login_view = 'auth.login'


@login_manager.user_loader
def load_user(user_id) -> UserModel:
    return UserModel.queryId(user_id=user_id)


def create_app() -> Flask:
    """ Crea una nueva instancia de la app """

    app = Flask(__name__)

    login_manager.init_app(app=app)

    app.register_blueprint(auth)

    return app
