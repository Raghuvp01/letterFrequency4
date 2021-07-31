from flask import Flask


def create_app():
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object("config.Config")

    # Initialize Plugins
    db.init_app(app)
    login_manager.init_app(app)
    sess.init_app(app)

    with app.app_context():
        from . import routes

        app.register_blueprint(routes.dashboard)
