import os
from dotenv import load_dotenv

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv()

GOOGLE_CLIENT_ID = (
    "1078691069630-8ad8lnoec0s1gjmk7pmltscmg8v813jt.apps.googleusercontent.com"
)
GOOGLE_CLIENT_SECRET = "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"


class Config(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    # GOOGLE_CLIENT_ID = os.getenv("GOOGLE_CLIENT_ID")
    # GOOGLE_CLIENT_SECRET = os.getenv("GOOGLE_CLIENT_SECRET")

    GOOGLE_CLIENT_ID = (
        "1078691069630-8ad8lnoec0s1gjmk7pmltscmg8v813jt.apps.googleusercontent.com"
    )
    GOOGLE_CLIENT_SECRET = "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"
    # for deployment on heroku
    # SQLALCHEMY_DATABASE_URI = os.environ.get("DATABASE_URL", "").replace(
    #     "postgres://", "postgresql://"
    # ) or "sqlite:///" + os.path.join(basedir, "app.db")

    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "app.db")

    SQLALCHEMY_TRACK_MODIFICATIONS = False
    LOG_TO_STDOUT = os.environ.get("LOG_TO_STDOUT")


class TestingConfig(object):
    SECRET_KEY = os.environ.get("SECRET_KEY") or "you-will-never-guess"
    SQLALCHEMY_DATABASE_URI = "sqlite:///" + os.path.join(basedir, "testdb.db")
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    GOOGLE_CLIENT_ID = (
        "1078691069630-8ad8lnoec0s1gjmk7pmltscmg8v813jt.apps.googleusercontent.com"
    )
    GOOGLE_CLIENT_SECRET = "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"
