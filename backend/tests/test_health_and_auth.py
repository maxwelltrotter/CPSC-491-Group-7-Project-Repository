from app import create_app


def setup_module():
    global app, client
    app = create_app()
    client = app.test_client()


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}
