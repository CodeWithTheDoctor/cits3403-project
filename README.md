# Web Akari
Web Akari is a web-based akari daily game for people to test out their puzzle-solving skills on a daily basis!

## Design
### Sign-in / Register Page
- This is the first page that appears when a user visits the website, given they aren't signed in yet.
- The user must have an account to play Web Akari

### Puzzle Page / Home Page
- Once signed in, they are redirected to the home page, i.e. the puzzle page.
- This is where the user can start the Akari puzzle of the day!
- When the "start" button is clicked, the timer begins.
- Pressing the submit button will check if the puzzle is solved or not. If it is, the time will be recorded and uploaded to the database.
  - If the puzzle is wrong, then the user will be informed.

### Statistics Page
- User can view the the number of puzzles they have solved, and their average solve time.

# Instructions to the run web app:
[Poetry](https://python-poetry.org/docs/) has been used as a python package manager but a requirements.txt file has been exported to use with a regular python venv


## Instructions for using a poetry build

### To install dependencies on local machine
`poetry install`

### To enter venv in terminal
`poetry shell`

### To spin up DEVELOPMENT server
- `poetry run flask run`

OR

- `poetry shell` <br>
- `flask run`

### To add dependencies
- `poetry add <pkgname>`

## Instructions for regular venv building
- `python3 -m venv .venv`
- `source .venv/bin/activate`
- `pip install -r requirements.txt`
- `flask run`

# Database commands
These commands need to be run when changes to the database schema are made.

- `flask db migrate -m <message>`
- `flask db upgrade`

# Testing
- `python3 -m pytest`

To run the coverage testing
- `python3 -m pytest --cov=app`
