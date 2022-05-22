import pytest
import os
from app import create_app, db, cli
from app.models import User, Puzzle, User_Puzzle


def populate_db():
    names = ["fred", "bob"]
    puzzles = ["123", "456", "789"]

    for name in names:
        user = User(username=name)
        user.set_password("password")
        db.session.add(user)

    for x in puzzles:
        x = Puzzle(config=x)
        db.session.add(x)

    up1 = User_Puzzle(user_id=1, puzzle_id=2, time=30)
    up2 = User_Puzzle(user_id=1, puzzle_id=1, time=20.4)

    db.session.add(up1)
    db.session.add(up2)
    db.session.commit()


@pytest.fixture(scope="session")
def app():
    app = create_app()

    cli.register(app)

    # create in memory database
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///"
    app.config["WTF_CSRF_ENABLED"] = False

    with app.app_context():
        db.drop_all()
        db.create_all()
        populate_db()

    yield app

    # clean up db after
    db.session.remove()
    db.drop_all()


@pytest.fixture(scope="session")
def client(app):
    app.testing = True
    ctx = app.app_context()
    ctx.push()
    return app.test_client()


@pytest.fixture
def runner(app):
    app.app_context().push()
    return app.test_cli_runner()


@pytest.fixture
def req_ctx(app):
    ctx = app.test_request_context()
    ctx.push()
    return app.test_client()


@pytest.fixture(scope="session")
def app_ctx(app):
    ctx = app.app_context()
    ctx.push()
    return app.test_client()


class AuthActions(object):
    def __init__(self, client):
        self._client = client

    def login(self, username="test", password="test"):
        return self._client.post(
            "/auth/login", data={"username": username, "password": password}
        )

    def logout(self):
        return self._client.get("/auth/logout")


@pytest.fixture
def auth(client):
    return AuthActions(client)
