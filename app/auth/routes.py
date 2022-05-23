from app.auth import bp
from flask import abort, render_template, redirect, url_for, flash, request
from werkzeug.urls import url_parse
from flask_login import login_user, logout_user, current_user
from app import db, oauth
from app.models import User
from app.auth.forms import LoginForm, RegistrationForm


@bp.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash("Invalid username or password")
            return redirect(url_for("auth.login"))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get("next")
        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("main.index")
        return redirect(next_page)
    return render_template("auth/login.html", title="Sign In", form=form)


@bp.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("main.index"))


@bp.route("/register", methods=["GET", "POST"])
def register():
    if current_user.is_authenticated:
        return redirect(url_for("main.index"))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash("Congratulations, you are now a registered user!")
        return redirect(url_for("auth.login"))
    return render_template("auth/register.html", title="Register", form=form)


@bp.route("")
def auth():
    """Redirect for google oauth, redirect to index after"""
    token = oauth.google.authorize_access_token()
    g_user = token.get("userinfo")

    if g_user:
        user = User.query.filter_by(email=g_user.email).first()
        if user is not None:
            login_user(user, remember=False)

        else:
            # create new user
            try:
                new_user = User(username=g_user.given_name, email=g_user.email)
                new_user.set_password("password")
                print("enter try block")
                db.session.add(new_user)
                db.session.commit()
                login_user(new_user, remember=False)
                next_page = request.args.get("next")
            except:
                abort(500)

        if not next_page or url_parse(next_page).netloc != "":
            next_page = url_for("main.index")
        return redirect(next_page)
    return redirect(url_for("main.index"))


@bp.route("/google")
def google():
    """Redirect uri for google oauth"""
    redirect_uri = url_for("auth.auth", _external=True)
    return oauth.google.authorize_redirect(redirect_uri)
