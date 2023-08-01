from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from os import path
from flask_login import LoginManager

db = SQLAlchemy()
DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'pacanele'
    app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DB_NAME}'
    #app.config['MESSAGE_FLASHING_OPTIONS'] = {'duration': 3}
    db.init_app(app)

    from .views import views
    from .auth import auth
    from .account import account
    from .admin import admin

    app.register_blueprint(views, url_prefix = '/')
    app.register_blueprint(auth, url_prefix = '/')
    app.register_blueprint(account, url_prefix = '/')
    app.register_blueprint(admin, url_prefix = '/')

    from .models import User

    with app.app_context():
        db.create_all()

    login_manager = LoginManager(app)
    login_manager.login_view = 'auth.login' # type: ignore
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
 
    return app
