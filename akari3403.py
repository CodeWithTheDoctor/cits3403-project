from distutils.command.config import config
from app import app, db
from app.models import User, Post, Puzzle, user_puzzles
from config import Config


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "User": User,
        "Post": Post,
        "Puzzle": Puzzle,
        "config": Config,
        "user_puzzles": user_puzzles,
    }
