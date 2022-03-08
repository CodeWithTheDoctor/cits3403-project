from flask import render_template
from app import app


@app.route("/")
@app.route("/index")
def index():
    user = {"username": "Miguel"}
    posts = [
        {"author": {"username": "john"}, "body": "Beautiful day in portland!"},
        {"author": {"username": "susan"}, "body": "The avengers movie was so cool!"},
    ]
    return render_template("index.html", title="Home", user=user, posts=posts)
