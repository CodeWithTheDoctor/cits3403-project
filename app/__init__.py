from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS
import click
import logging

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)
login = LoginManager(app)
login.login_view = "login"  # pass flask-login the view function
CORS(app)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
app.logger.addHandler(stream_handler)
app.logger.setLevel(logging.DEBUG)

# def create_app(config_class=Config):
# if not app.debug and not app.testing:
#     if app.config["LOG_TO_STDOUT"]:
#         stream_handler = logging.StreamHandler()
#         stream_handler.setLevel(logging.INFO)
#         app.logger.addHandler(stream_handler)
#     else:
#         if not os.path.exists("logs"):
#             os.mkdir("logs")
#         file_handler = logging.RotatingFileHandler(
#             "logs/akari3403.log", maxBytes=10240, backupCount=10
#         )
#         file_handler.setFormatter(
#             logging.Formatter(
#                 "%(asctime)s %(levelname)s: %(message)s " "[in %(pathname)s:%(lineno)d]"
#             )
#         )
#         file_handler.setLevel(logging.INFO)
#         app.logger.addHandler(file_handler)

#     app.logger.setLevel(logging.INFO)
#     app.logger.info("Akari startup")
#     # return app
from app.models import Puzzle


@app.cli.command("add-puzzle")
@click.argument("config")
def add_puzzle(config):
    """Enter the config for a new puzzle"""
    p = Puzzle(config=config)
    try:
        db.session.add(p)
        db.session.commit()
        print("Puzzle successfully added")
    except:
        print("Error adding new puzzle")
        db.session.rollback()
