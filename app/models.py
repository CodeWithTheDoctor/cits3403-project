from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    score = db.Column(db.Integer, index=True)
    puzzles = db.relationship("User_Puzzle", back_populates="user")

    def set_password(self, password) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return "<User {}>".format(self.username)


class Puzzle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    config = db.Column(db.String(150), unique=True)
    users = db.relationship("User_Puzzle", back_populates="puzzle")


class User_Puzzle(db.Model):
    user_id = db.Column(db.ForeignKey(User.id), primary_key=True, autoincrement=False)
    puzzle_id = db.Column(
        db.ForeignKey(Puzzle.id), primary_key=True, autoincrement=False
    )
    time = db.Column(db.Float)
    puzzle = db.relationship("Puzzle", back_populates="users")
    user = db.relationship("User", back_populates="puzzles")

    def to_dict(self):
        data = {"user_id": self.user_id, "puzzle_id": self.puzzle_id, "time": self.time}
        return data
