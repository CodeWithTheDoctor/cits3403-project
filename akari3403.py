from app import app, db, cli, create_app
from app.main import routes
from app.models import User, Puzzle, User_Puzzle
from config import Config

app = create_app()
cli.register(app)


@app.shell_context_processor
def make_shell_context():
    return {
        "db": db,
        "User": User,
        "config": Config,
        "Puzzle": Puzzle,
        "User_Puzzle": User_Puzzle,
        "routes": routes,
        "submit_puzzle": routes.submit_puzzle,
        "populate_db": populate_db,
    }
