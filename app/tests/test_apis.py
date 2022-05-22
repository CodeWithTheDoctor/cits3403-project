def test_leaderboard(app_ctx):
    response = app_ctx.get("/api/leaderboard/1")

    assert response.status_code == 200


def test_user_statistics(app_ctx):
    response = app_ctx.get("/api/user/david/statistics")

    assert response.status_code == 200
    assert "username" in response.data


def test_non_existent_user(app_ctx):
    response = app_ctx.get("/api/user/johnthethird12345/statistics")

    assert response.status_code == 404
