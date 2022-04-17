from datetime import datetime
from app import db, login
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.dialects.postgresql import ARRAY


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


user_puzzles = db.Table(
    "user_puzzles",
    db.Column("puzzle_id", db.Integer, db.ForeignKey("puzzle.id"), primary_key=True),
    db.Column("user_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
)


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True)
    email = db.Column(db.String(120), index=True, unique=True)
    password_hash = db.Column(db.String(128))
    posts = db.relationship("Post", backref="author", lazy="dynamic")
    puzzles = db.relationship(
        "Puzzle",
        secondary=user_puzzles,
        lazy="subquery",
        backref=db.backref("puzzles", lazy=True),
    )

    def set_password(self, password) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password) -> bool:
        return check_password_hash(self.password_hash, password)

    def __repr__(self) -> str:
        return "<User {}>".format(self.username)


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    def __repr__(self) -> str:
        return "<Post {}>".format(self.body)


class Puzzle(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    board = db.Column(ARRAY(db.Integer, dimensions=2))
    score = db.Column(db.Integer, nullable=False)
    dimension = db.Column(db.Integer)

    def __repr__(self) -> str:
        return "<Puzzle {}>".format(self.board)
