def test_index_redirects_to_login(my_client):
    response = my_client.get("/")

    assert response.status_code == 302
    assert response.request.path == "/"


def test_login_page_with_anonymous(my_client):
    response = my_client.get("/auth/login")

    assert response.status_code == 200
    assert b"Akari 3403" in response.data


def test_register_form(my_client):
    data = {
        "username": "Bran",
        "password": "secretpassword",
        "email": "bran@example.com",
    }

    response = my_client.post("/register", data=data)
    assert response.status_code == 200
