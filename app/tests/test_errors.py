from flask import abort
import pytest
from werkzeug.exceptions import InternalServerError


def test_returns_404(app_ctx):
    response = app_ctx.get("/nothing", follow_redirects=True)
    assert response.status_code == 404
    assert "The administrator has been notified"


def test_returns_500(app_ctx):
    with pytest.raises(InternalServerError):
        abort(500)
