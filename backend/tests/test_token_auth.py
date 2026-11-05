import time

from itsdangerous import TimestampSigner, URLSafeTimedSerializer

USERNAME = "tokenuser"
PASSWORD = "Str0ng!Passw0rd#"


def get_token(client):
    client.post("/api/auth/register", json={"username": USERNAME, "password": PASSWORD})
    response = client.post("/api/auth/login", json={"username": USERNAME, "password": PASSWORD})
    return response.get_json()["access_token"]


def test_me_without_token_returns_401(client):
    response = client.get("/api/auth/me")
    assert response.status_code == 401


def test_me_with_wrong_token_returns_401(client):
    response = client.get("/api/auth/me", headers={"Authorization": "Bearer fake-token"})
    assert response.status_code == 401


def test_me_with_valid_token_returns_200(client):
    token = get_token(client)
    response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 200
    assert response.get_json()["username"] == USERNAME


def test_me_with_expired_token_returns_401(client, monkeypatch):
    token = get_token(client)
    monkeypatch.setattr("app.routes.auth.TOKEN_MAX_AGE", -1)
    response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401


def test_me_with_token_older_than_one_hour_returns_401(client, monkeypatch):
    # make a token that looks like it was created 3601 seconds ago
    # TOKEN_MAX_AGE stays at the normal 3600
    old_time = int(time.time()) - 3601
    with monkeypatch.context() as m:
        m.setattr(TimestampSigner, "get_timestamp", lambda self: old_time)
        token = get_token(client)

    response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401


def test_me_with_valid_token_for_missing_user_returns_401(client, app):
    # a correctly signed token, but the user id does not exist
    serializer = URLSafeTimedSerializer(app.config["SECRET_KEY"])
    token = serializer.dumps({"user_id": 99999})

    response = client.get("/api/auth/me", headers={"Authorization": f"Bearer {token}"})
    assert response.status_code == 401
