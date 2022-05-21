from flask import (
    jsonify,
    request,
    abort,
)
from sqlalchemy.exc import IntegrityError
from app import app, db, errors
from flask_login import current_user, login_required
from app.models import User, User_Puzzle, Puzzle
from app.api import bp
from app.api import validate_puzzle, check_puzzle

import random
import datetime
import dotsi


@bp.route("/<int:puzzle_id>/leaderboard", methods=["GET"])
def leaderboard(puzzle_id):
    query = (
        User_Puzzle.query.filter_by(puzzle_id=puzzle_id)
        .order_by(User_Puzzle.time)
        .all()
    )

    leaderboard = [
        {"username": entry.user.username, "time": entry.time} for entry in query
    ]

    response = jsonify(leaderboard)
    response.status_code = 200
    return response


@bp.route("/user/<username>/statistics")
@login_required
def statistics(username):

    user = User.query.filter_by(username=username).first_or_404()
    query = User_Puzzle.query.filter_by(user_id=user.id).all()
    times = [puzzle.time for puzzle in query]

    # default large number to stop missing error
    average = 10000

    if not times:
        # prevent division by zero error when no puzzles
        average = sum(times) / len(times)

    num_puzzles = len(query)

    stats = {"username": user.username, "average": average, "num_puzzles": num_puzzles}

    response = jsonify(stats)
    response.status_code = 200


# @bp.route("/api/admin/add", methods=["POST"])
# def add_puzzle(config: str) -> dict:
#     if not validate_puzzle(config):
#         app.logger.info("Puzzle is invalid")
#         return errors.bad_request("Puzzle is invalid")
#     else:
#         try:
#             new_puzzle = Puzzle(config=config)
#             db.session.add(new_puzzle)
#             db.session.commit()
#             app.logger.info("New puzzle succesfully added.")
#             response = jsonify({"config": config})
#             response.status_code = 201
#         except:
#             db.session.rollback()
#             response = errors.bad_request("error adding puzzle")
#         finally:
#             return response


@bp.route("/api/puzzle/<user_id>", methods=["GET"])
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


@login_required
@bp.route("/api/puzzle/submit", methods=["POST"])
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
            pass
            # FIXME: comment out while testing
            # return errors.bad_request("Must include user_id, puzzle_id and time")
    user_id, puzzle_id, time = data

    if check_puzzle():
        entry = User_Puzzle(time=time, puzzle_id=puzzle_id, user_id=user_id)
        try:
            db.session.add(entry)
            # db.session.commit()
            data = entry.to_dict()
            response = jsonify(data)
            response.status_code = 201

        except IntegrityError:
            app.logger.error("Duplicate entry exists")
            db.session.rollback()
            response = errors.bad_request("Duplicate entry exists")

        finally:
            db.session.rollback()
            return response

    else:
        abort(403)
