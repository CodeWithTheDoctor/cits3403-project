import pytest
import os
from app import app, db
from app.models import User, Puzzle, User_Puzzle
import unittest


def populate_db():
    names = ["henry", "lateesha", "susan"]
    puzzles = ["123", "345", "456", "789"]

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


# @pytest.fixture()
# def app():
#     basedir = os.path.abspath(os.path.dirname(__file__))

#     app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
#         basedir, "testdb"
#     )

#     app = app.test_client()
#     db.create_all()
#     populate_db()
#     yield app


class StudentModelCase(unittest.TestCase):
    def setUp(self):
        basedir = os.path.abspath(os.path.dirname(__file__))
        self.app = app.test_client()
        app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
            basedir, "testdb"
        )

        db.create_all()
        populate_db()

    def tearDown(self):
        db.session.remove()
        db.drop_all()

    def test_one(self):
        u = User.query.first()
        self.assertTrue(u.username == "henry")


def main():
    unittest.main()


if __name__ == "main":
    main()
