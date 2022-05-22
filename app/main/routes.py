from flask import redirect, render_template, url_for
from flask_login import login_required, current_user
from app.main import bp
from app import db, oauth

from datetime import datetime


@bp.before_app_request
def before_request():
    # if current_user.is_authenticated:
    #     last = current_user.last_seen
    #     now = datetime.utcnow()
    #     days = (now - last) / days

    #     if days == 1:
    #         current_user.streak += 1
    #     current_user.last_seen = datetime.utcnow()

    #     db.session.commit()
    pass


@bp.route("/")
@bp.route("/index")
@login_required
def index():
    return render_template("index.html", title="Home")
