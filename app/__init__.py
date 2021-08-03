from flask import Flask
from flask_login import LoginManager
from flask_session import Session
from flask_sqlalchemy import SQLAlchemy
from ddtrace import patch_all
from flaskext.mysql import MySQL
from pymysql.cursors import DictCursor

db = SQLAlchemy()
login_manager = LoginManager()
sess = Session()
patch_all()
mysql = MySQL(cursorclass=DictCursor)


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.Config")

    db.init_app(app)
    login_manager.init_app(app)
    sess.init_app(app)
    mysql.init_app(app)

    with app.app_context():
        from . import routes
        from . import auth
        from .assets import compile_static_assets, compile_auth_assets

        app.register_blueprint(routes.home_bp)
        app.register_blueprint(auth.auth_bp)

        compile_static_assets(app)
        compile_auth_assets(app)

        db.create_all()

        return app
