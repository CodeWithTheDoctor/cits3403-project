import pytest
import os
from app import create_app, db, cli
from app.models import User, Puzzle, User_Puzzle
from pathlib import Path


def populate_db():
    names = ["fred", "bob"]
    puzzles = ["123", "456", "789"]

    for name in names:
        user = User(username=name)
        db.session.add(user)

    for x in puzzles:
        x = Puzzle(config=x)
        db.session.add(x)

    up1 = User_Puzzle(user_id=1, puzzle_id=2, time=30)
    up2 = User_Puzzle(user_id=1, puzzle_id=1, time=20.4)

    db.session.add(up1)
    db.session.add(up2)
    db.session.commit()


@pytest.fixture
def app():
    app = create_app()
    app.testing = True
    cli.register(app)

    # create in memory database
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"

    app.app_context().push()
    db.drop_all()
    db.create_all()
    populate_db()

    yield app

    # clean up db after
    db.session.remove()
    db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()


@pytest.fixture
def my_client():
    app = create_app()
    app.app_context().push
    app.testing = True
    return app.test_client()
