# Authors

- Sean Peralta Garcia - 23088091 
- Ashish Manoj Ithape - 23066342
- Shao-ming Tan 20920822
- Jummanah - 23087282

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
  - Submitting the puzzle successfuly will pull up a modal showing your time, and the top 5 people on the leaderboard, as well as a section to share your score on social media platforms


### Statistics Page
- User can view the the number of puzzles they have solved, and their average solve time.

# Instructions to the run web app:
[Poetry](https://python-poetry.org/docs/) has been used as a python package manager but a requirements.txt file has been exported to use with a regular python venv (virtual environment).


## Instructions for using a poetry build

### To install dependencies on local machine
`poetry install`

### To enter venv in terminal
`poetry shell`

### To run the DEVELOPMENT server
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

# Adding/Viewing/Deleting Puzzles

## Structure of a puzzle string
**Example file**: 
```
03 213 33 435 63
30
326
34 52

14
```

- The first line indicates the locations of all the black squares. [(0,3), (2,1), (2,3), (3,3), (4,3), (4,5), (6,3)]
- The second line indicates the position of all the '0' black squares. [(3,0)]
- The third line indicates the position of all the '1' black squares. [(3,2), (3,6)]
- The fourth line indicates the position of all the '2' black squares. [(3,4), (5,2)]
- The fifth line indicates the position of all the '3' black squares. [There's none]
- The sixth line indicates the position of all the '4' black squares. [(1,4)]

We rewrite that line, using `z` as the new-line separator, so the puzzle level string becomes: `03 213 33 435 63z30z326z34 52zz14`

### Adding a puzzle to the database
- Ensure that poetry shell is running (`poetry shell`)
- Use the command `flask add-puzzle <puzzle-string>` to add the puzzle
- eg: `flask add-puzzle 03 213 33 435 63z30z326z34 52zz14`

### Viewing puzzles
- `flask puzzles`

### Deleting puzzles
- `flask remove-puzzle <puzzle-id>`

# For developers
### Database commands
These commands need to be run when changes to the database schema are made. (Changes mean changes to the table, like the columns, etc. Adding new records to the table doesn't count as a change)

- `flask db migrate -m <message>`
- `flask db upgrade`

### Testing
- `python3 -m pytest`

To run the coverage testing
- `python3 -m pytest --cov=app`
