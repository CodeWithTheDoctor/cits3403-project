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
