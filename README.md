# env

# To install dependencies
poetry install

# To enter venv in terminal
poetry shell

# To spin up server
poetry run flask run

OR

poetry shell
flask run

# To add dependencies
poetry add pkgname

# On change to databse ( in venv )
flask db migrate
flask db upgrade

# db notes
An unfortunate problem with recent versions of SQLAlchemy is that they expect Postgres database URLs to begin with postgresql://, instead of the postgres:// that Heroku uses. To ensure that the application can connect to the database, it is necessary to update the URL to the format required by SQLAlchemy. This can be done with a string replacement operation in the Config class:


class Config(object):
    # ...
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL', '').replace(
        'postgres://', 'postgresql://') or \
        'sqlite:///' + os.path.join(basedir, 'app.db')
    # ...

# check logging
