# Akari

# Instructions to the run web app:

### Environment Variables
- Add environment variables to the '.flaskenv' file

### To install dependencies on local machine
`poetry install`

### To enter venv in terminal
`poetry shell`

### To spin up DEVELOPMENT server
- `poetry run flask run`

OR

- `poetry shell` <br>
`flask run`

### To add dependencies
- `poetry add <pkgname>`

### On change to databse
- `flask db migrate`
- `flask db upgrade`

# On change to databse
- flask db migrate
- flask db upgrade


# Testing
- python3 -m pytest
- python3 -m pytest --cov=app
