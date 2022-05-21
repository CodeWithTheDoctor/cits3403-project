from app import app, db, routes, cli, create_app
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


def populate_db():
    names = ["henry", "lateesha", "susan"]
    puzzles = ["123", "345", "456", "789"]

    for name in names:
        user = User(username=name)
        db.session.add(user)
        db.session.commit()

    for x in puzzles:
        x = Puzzle(config=x)
        db.session.add(x)
        db.session.commit()

    up1 = User_Puzzle(user_id=1, puzzle_id=2, time=30)
    up2 = User_Puzzle(user_id=1, puzzle_id=1, time=20.4)

    db.session.add(up1)
    db.session.add(up2)
    db.session.commit()
