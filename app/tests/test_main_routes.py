from flask import session, g
from app.auth.forms import RegistrationForm
from app.models import User


def test_index_redirects_to_login(app_ctx):
    response = app_ctx.get("/")

    assert response.status_code == 302
    assert response.request.path == "/"


def test_login_page_with_anonymous(app_ctx):
    response = app_ctx.get("/auth/login")

    assert response.status_code == 200
    assert b"Akari 3403" in response.data


def test_register_form_submits_to_db(app_ctx):
    response = app_ctx.post(
        "/auth/register",
        data={
            "username": "Bran",
            "password": "secretpassword",
            "password2": "secretpassword",
            "email": "bran@example.com",
        },
    )

    assert response.status_code == 302
    assert response.headers["location"] == "/auth/login"

    u1 = User.query.filter_by(username="Bran").first()

    assert u1.username == "Bran"


def test_modify_session(req_ctx, app_ctx):

    response = app_ctx.get("/auth/login")

    response = app_ctx.post(
        "/auth/login",
        data={"username": "fred", "password": "password", "remember_me": False},
        follow_redirects=True,
    )

    assert response.status_code == 200
    assert response.request.path == "/index"
