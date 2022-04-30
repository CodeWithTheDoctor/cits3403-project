# env
add environment variable to .flaskenv

# To install dependencies on local machine
poetry install

# To enter venv in terminal
poetry shell

# To spin up DEVELOPMENT server
poetry run flask run

OR

poetry shell
flask run

# To add dependencies
poetry add <pkgname>

# On change to databse
flask db migrate
flask db upgrade
