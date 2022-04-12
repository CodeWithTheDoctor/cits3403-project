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
