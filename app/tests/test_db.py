from app.models import User, Puzzle, User_Puzzle
from conftest import client


def test_can_query_user(client):
    u = User.query.first()
    assert u.username == "fred"


def test_index(my_client):
    response = my_client.get("/")
    html = response.data.decode()
    print(html)
    assert response.status_code == 200
    assert b"Hi!" in response.data
