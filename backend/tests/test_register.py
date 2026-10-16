from app.models.user import User


def register(client, username="alice", password="Abcdef1!"):
    return client.post(
        "/api/auth/register",
        json={"username": username, "password": password},
    )


def test_register_success(client):
    response = register(client)
    assert response.status_code == 201
    assert response.get_json()["username"] == "alice"


def test_register_stores_hashed_password(client, app):
    register(client)
    with app.app_context():
        user = User.query.filter_by(username="alice").first()
        assert user is not None
        assert user.password_hash != "Abcdef1!"
        assert user.password_hash.startswith(("scrypt:", "pbkdf2:"))


def test_register_weak_password_rejected(client):
    response = register(client, password="abc")
    assert response.status_code == 400
    assert "details" in response.get_json()


def test_register_duplicate_username_rejected(client):
    register(client)
    response = register(client)
    assert response.status_code == 409


def test_register_missing_username_rejected(client):
    response = client.post("/api/auth/register", json={"password": "Abcdef1!"})
    assert response.status_code == 400