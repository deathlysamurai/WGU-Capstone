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
    from .controllers.pantry import pantry
    from .controllers.meals import meals
    from .controllers.shopping import shopping
    from .controllers.admin.admin import admin
    from .controllers.admin.admin_users import admin_users
    from .controllers.admin.admin_foods import admin_foods
    from .controllers.admin.admin_units import admin_units
    from .controllers.admin.admin_user_foods import admin_user_foods
    from .controllers.admin.admin_meals import admin_meals
    from .controllers.admin.admin_meal_foods import admin_meal_foods

    app.register_blueprint(general, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')
    app.register_blueprint(pantry, url_prefix='/pantry')
    app.register_blueprint(meals, url_prefix='/meals')
    app.register_blueprint(shopping, url_prefix='/shopping')
    app.register_blueprint(admin, url_prefix='/admin/')
    app.register_blueprint(admin_users, url_prefix='/admin/users')
    app.register_blueprint(admin_foods, url_prefix='/admin/foods')
    app.register_blueprint(admin_units, url_prefix='/admin/units')
    app.register_blueprint(admin_user_foods, url_prefix='/admin/user_foods')
    app.register_blueprint(admin_meals, url_prefix='/admin/meals')
    app.register_blueprint(admin_meal_foods, url_prefix='/admin/meal_foods')

    from .models import User
    from .data_loaders.load_data import run_data_loaders

    create_database(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(id):
        return User.query.get(int(id))
    
    run_data_loaders(app, db)

    return app

def create_database(app):
    if not os.path.exists('website/' + DB_NAME):
        with app.app_context():
            reset_database()
            db.create_all()
            print('Created Database')

def reset_database():
    db.drop_all() #RESET DATABASE
    print('DATABASE RESET')