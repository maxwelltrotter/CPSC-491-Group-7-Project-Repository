def register(client, username="alice", password="Abcdef1!"):
    return client.post(
        "/api/auth/register",
        json={"username": username, "password": password},
    )


def login(client, username="alice", password="Abcdef1!"):
    return client.post(
        "/api/auth/login",
        json={"username": username, "password": password},
    )


def test_login_success(client):
    register(client)
    response = login(client)
    assert response.status_code == 200
    assert response.get_json()["username"] == "alice"


def test_login_wrong_password_fails(client):
    register(client)
    response = login(client, password="Wrong1234!")
    assert response.status_code == 401


def test_wrong_password_and_unknown_user_give_same_error(client):
    register(client)
    wrong_password = login(client, password="Wrong1234!")
    unknown_user = login(client, username="nobody")
    assert wrong_password.status_code == unknown_user.status_code
    assert wrong_password.get_json() == unknown_user.get_json()


def test_account_locks_after_five_bad_tries(client):
    register(client)
    for _ in range(5):
        login(client, password="Wrong1234!")
    response = login(client)
    assert response.status_code == 423


def test_good_login_resets_failed_attempts(client):
    register(client)
    for _ in range(4):
        login(client, password="Wrong1234!")
    assert login(client).status_code == 200
    for _ in range(4):
        login(client, password="Wrong1234!")
    assert login(client).status_code == 200


def test_login_missing_fields_fails(client):
    response = client.post("/api/auth/login", json={})
    assert response.status_code == 401