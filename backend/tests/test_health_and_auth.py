from app import create_app


def setup_module():
    global app, client
    app = create_app()
    client = app.test_client()


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_register_stub():
    response = client.post(
        "/api/auth/register",
        json={"username": "testuser", "password": "testpass123"},
    )
    assert response.status_code == 201
    data = response.get_json()
    assert data["message"] == "register endpoint reached"


def test_login_stub():
    response = client.post(
        "/api/auth/login",
        json={"username": "testuser", "password": "testpass123"},
    )
    assert response.status_code == 200
    data = response.get_json()
    assert data["message"] == "login endpoint reached"