from flask import Flask
from config import Config
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_cors import CORS
import click
import logging, os
import logging.handlers


db = SQLAlchemy()
migrate = Migrate()
login = LoginManager()
login.login_view = "login"  # pass flask-login the view function
cors = CORS()

# stream_handler = logging.StreamHandler()
# stream_handler.setLevel(logging.DEBUG)
# app.logger.addHandler(stream_handler)
# app.logger.setLevel(logging.DEBUG)


def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    login.init_app(app)
    cors.init_app(app)

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


app = create_app()

from app.models import Puzzle, User


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


@app.cli.command("delete-puzzle")
@click.argument("puzzle_id")
def delete_puzzle(puzzle_id):
    """Delete puzzle by  id"""

    p = Puzzle.query.get(puzzle_id)

    if p is None:
        print(f"ERROR: No puzzle exists by {puzzle_id}")
        return

    try:
        db.session.delete(p)
        db.session.commit()
        print(f"Puzzle: {puzzle_id} successfuly deleted")
    except Exception as e:
        print("Error encountered while deleting")
        print(e)


@app.cli.command("puzzles")
def puzzles():
    """Show all puzzles"""
    puzzles = Puzzle.query.all()

    for puzzle in puzzles:
        print(f"Puzzle: {puzzle.id} has config {puzzle.config}")


@app.cli.command("users")
def users():
    """Show all users"""
    users = User.query.all()

    for user in users:
        print(f"Puzzle: {user.id} has username {user.username}")


@app.cli.command("delete-user")
@click.argument("user_id")
def delete_user(user_id):
    """Delete user by id"""
    u = User.query.get(user_id)

    if u is None:
        print(f"ERROR: No puzzle exists by {user_id}")
        return

    try:
        db.session.delete(u)
        db.session.commit()
        print(f"Puzzle: {user_id} successfuly deleted")
    except Exception as e:
        print("Error encountered while deleting")
        print(e)
