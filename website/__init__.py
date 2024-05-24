import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from dotenv import load_dotenv

db = SQLAlchemy()
load_dotenv()
DB_NAME = os.environ.get("DB_URL")

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = os.environ.get("SEC_KEY")
    app.config['SQLALCHEMY_DATABASE_URI'] = DB_NAME
    db.init_app(app)

    from .controllers.general import general
    from .controllers.auth import auth

    app.register_blueprint(general, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    from .models import User

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))

    return app

def create_database(app):
    if not os.path.exists('website/' + DB_NAME):
        with app.app_context():
            db.create_all()
            print('Created Database')