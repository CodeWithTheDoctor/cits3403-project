from distutils.command.config import config
from app import app, db, routes
from app.models import User, Puzzle, User_Puzzle
from config import Config


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "User": User,
        "config": Config,
        "Puzzle": Puzzle,
        "User_Puzzle": User_Puzzle,
        "routes": routes,
    }
