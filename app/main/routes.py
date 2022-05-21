from flask import render_template
from flask_login import login_required, current_user
from app.main import bp
from app import db

from datetime import datetime


@bp.before_app_request
def before_request():
    if current_user.is_authenticated:
        last = current_user.last_seen
        now = datetime.utcnow()
        days = (now - last) / days

        if days == 1:
            current_user.streak += 1
        current_user.last_seen = datetime.utcnow()

        db.session.commit()


@bp.route("/")
@bp.route("/index")
@login_required
def index():
    return render_template("index.html", title="Home")
