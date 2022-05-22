from app.auth.forms import RegistrationForm
from app.models import User, Puzzle, User_Puzzle
from app import db


def test_can_query_user(client):
    "Assert that the db can be queried for user"
    u = User.query.first()
    assert u.username == "fred"


def test_register_user(client):
    """Test a user can be added to the db"""
    u = User(username="henry")
    u.set_password("password")
    db.session.add(u)

    assert u in User.query.all()


def test_password_hash(client):
    """Test that the user's password is not in plain text"""
    u = User(username="henry")
    u.set_password("password")
    assert u.password_hash != "password"


def test_up_updates_user(client):
    up = User_Puzzle(user_id=2, puzzle_id=1, time=30.0)
    db.session.add(up)

    user = User.query.get(2)

    assert up in user.puzzles
