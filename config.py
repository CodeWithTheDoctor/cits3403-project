import os

basedir = os.path.abspath(os.path.dirname(__file__))

# TODO: check what the secret_key does
class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"

    # development
    # SQLALCHEMY_DATABASE_URI = os.environ.get(
    #     "DATABASE_URL"
    # ) or "sqlite:///" + os.path.join(basedir, "app.db")
    #

    # heroku testing
    SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "").replace(
        "postgres://", "postgresql://"
    ) or "sqlite:///" + os.path.join(basedir, "app.db")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_TO_STDOUT = os.environ.get("LOG_TO_STDOUT")
