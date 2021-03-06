from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS
import logging, os
import logging.handlers
from authlib.integrations.flask_client import OAuth


oauth = OAuth()
db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = "auth.login"  # pass flask-login the view function
cors = CORS()


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    cors.init_app(app)
    oauth.init_app(app)

    from app.errors import bp as errors_bp

    app.register_blueprint(errors_bp, url_prefix="/error")

    from app.auth import bp as auth_bp

    app.register_blueprint(auth_bp, url_prefix="/auth")

    from app.main import bp as main_bp

    app.register_blueprint(main_bp)

    from app.api import bp as api_bp

    app.register_blueprint(api_bp, url_prefix="/api")

    if not app.debug and not app.testing:
        if app.config["LOG_TO_STDOUT"]:
            stream_handler = logging.StreamHandler()
            stream_handler.setLevel(logging.INFO)
            app.logger.addHandler(stream_handler)
        else:
            if not os.path.exists("logs"):
                os.mkdir("logs")
            file_handler = logging.handlers.RotatingFileHandler(
                "logs/akari3403.log", maxBytes=10240, backupCount=10
            )
            file_handler.setFormatter(
                logging.Formatter(
                    "%(asctime)s %(levelname)s: %(message)s "
                    "[in %(pathname)s:%(lineno)d]"
                )
            )
            file_handler.setLevel(logging.INFO)
            app.logger.addHandler(file_handler)

        app.logger.setLevel(logging.INFO)
        app.logger.info("Akari startup")

    return app


from app import models
