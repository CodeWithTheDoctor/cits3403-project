from flask import render_template, flash, redirect, url_for, request
from app import app, db
from app.forms import LoginForm
from flask_login import current_user, login_required, login_user, logout_user
from app.models import User, User_Puzzle
from werkzeug.urls import url_parse
from app.forms import RegistrationForm


@app.route("/")
@app.route("/index")
@login_required
def index():
    posts = [
        {"author": {"username": "john"}, "body": "Beautiful day in portland!"},
        {"author": {"username": "susan"}, "body": "The avengers movie was so cool!"},
    ]
    return render_template("index.html", title="Home", posts=posts)


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


@app.route("/<puzzle_id>/leaderboard", methods=["GET"])
def leaderboard(puzzle_id):

    query = (
        User_Puzzle.query.filter_by(puzzle_id=puzzle_id)
        .order_by(User_Puzzle.time)
        .all()
    )

    leaderboard = [{"username": user.user_id, "time": user.time} for user in query]

    return render_template(
        "leaderboard.html", title="Leaderboard", leaderboard=leaderboard
    )


@app.route("/user/<username>/statistics")
@login_required
def statistics(username):

    current_user = User.query.filter_by(username=username).first_or_404()

    # top = User.query.order_by(score).limit(10)

    # FIXME: This top is a mock return object
    top = [
        {"username": "henry", "score": 1300, "puzzles": 1},
        {"username": "david", "score": 1200, "puzzles": 2},
        {"username": "alexis", "score": 1000, "puzzles": 3},
    ]

    return render_template(
        "statistics.html", title="Statistics", user=current_user, top=top
    )
