from flask import (
    jsonify,
    render_template,
    flash,
    redirect,
    url_for,
    request,
    abort,
)
from sqlalchemy.exc import IntegrityError
from app import app, db, errors
from app.forms import LoginForm
from flask_login import current_user, login_required, login_user, logout_user
from app.models import User, User_Puzzle, Puzzle
from werkzeug.urls import url_parse
from app.forms import RegistrationForm

import random
import datetime
import dotsi


@app.route("/")
@app.route("/index")
@login_required
def index():
    return render_template("index.html", title="Home")


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("index")
        return redirect(next_page)
    return render_template("login.html", title="Sign In", form=form)


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("login"))
    return render_template("register.html", title="Register", form=form)


# TODO: Convert to an api route?
@app.route("/<puzzle_id>/leaderboard", methods=["GET"])
def leaderboard(puzzle_id):
    # TODO: Check referring url
    query = (
        User_Puzzle.query.filter_by(puzzle_id=puzzle_id)
        .order_by(User_Puzzle.time)
        .all()
    )

    leaderboard = [
        {"username": entry.user.username, "time": entry.time} for entry in query
    ]

    return render_template(
        "leaderboard.html",
        title="Leaderboard",
        leaderboard=leaderboard,
        puzzle_id=puzzle_id,
    )


# TODO: Convert to an api route?
@app.route("/user/<username>/statistics")
@login_required
def statistics(username):
    # FIXME: division by zero error when notimes listed

    user = User.query.filter_by(username=username).first_or_404()
    query = User_Puzzle.query.filter_by(user_id=user.id).all()
    times = [puzzle.time for puzzle in query]

    if not times:
        average = sum(times) / len(times)

    num_puzzles = len(query)

    stats = {"username": user.username, "average": average, "num_puzzles": num_puzzles}

    return render_template("statistics.html", title="Statistics", stats=stats)


"""
API Routes defined from here
"""


def validate_puzzle(config: str) -> bool:
    """
    Serverside validation of the puzzle
    """
    pass


@app.route("/api/admin/add", methods=["POST"])
def add_puzzle(config: str) -> dict:
    if not validate_puzzle(config):
        app.logger.info("Puzzle is invalid")
        return errors.bad_request("Puzzle is invalid")
    else:
        try:
            new_puzzle = Puzzle(config=config)
            db.session.add(new_puzzle)
            db.session.commit()
            app.logger.info("New puzzle succesfully added.")
            response = jsonify({"config": config})
            response.status_code = 201
        except:
            db.session.rollback()
            response = errors.bad_request("error adding puzzle")
        finally:
            return response


@app.route("/api/puzzle/<user_id>", methods=["GET"])
def get_puzzle(user_id):
    """
    Returns the config for a random puzzle from the list of unsolved puzzles of a user
    Uses pseudorandom date as seed so will return the same puzzle for the day

        Parameters:
            user_id (int): id of user to fetch unsolved puzzles

    response structure:
    {
        "config":
    }
    """

    seed = int(datetime.datetime.today().strftime("%Y%m%d"))
    random.seed(seed)

    done_puzzles = User.query.filter_by(id=user_id).first_or_404().puzzles
    done_puzzles = [puzzle.puzzle_id for puzzle in done_puzzles]

    all_puzzles = Puzzle.query.all()
    puzzle_ids_all = [puzzle.id for puzzle in all_puzzles]

    choices = list(set(puzzle_ids_all).difference(done_puzzles))

    choice = random.choice(choices)
    data = {"config": Puzzle.query.get(choice).config}
    response = jsonify(data)
    response.status_code = 200
    return response


@app.route("/api/puzzle/submit", methods=["POST"])
def submit_puzzle():
    # TODO: add some sort of authentication?
    """
    request structures:
    {
        "user_id':
        "puzzle_id":
        "time":
        "solution": TODO: Implement this
    }
    """

    data = dotsi.fy(request.get_json()) or {}
    for required in ("user_id", "puzzle_id", "time"):
        if required not in data:
            return errors.bad_request("Must include user_id, puzzle_id and time")


    user_id = data.user_id
    puzzle_id = data.puzzle_id
    time = float(data.time)

    if check_puzzle():
        print('checking')
        entry = User_Puzzle(time=time, puzzle_id=puzzle_id, user_id=user_id)

        try:
            db.session.add(entry)
            db.session.commit()
            data = entry.to_dict()
            response = jsonify(data)
            response.status_code = 201

        except IntegrityError:
            app.logger.error("Duplicate entry exists")
            db.session.rollback()
            response = errors.bad_request("Duplicate entry exists")

        finally:
            return response

    else:
        abort(403)


def check_puzzle() -> bool:
    return True
