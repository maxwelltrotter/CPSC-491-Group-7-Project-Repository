def test_unknown_route_returns_json_error(client):
    response = client.get("/no-such-route")
    assert response.status_code == 404
    assert "error" in response.get_json()


def test_wrong_method_returns_json_error(client):
    response = client.get("/api/auth/login")
    assert response.status_code == 405
    assert "error" in response.get_json()


def test_allowed_origin_gets_cors_headers(client):
    origin = "http://localhost:3000"
    response = client.get("/health", headers={"Origin": origin})
    assert response.headers["Access-Control-Allow-Origin"] == origin


def test_unknown_origin_gets_no_cors_headers(client):
    response = client.get("/health", headers={"Origin": "http://evil.example"})
    assert "Access-Control-Allow-Origin" not in response.headers


def test_preflight_allows_authorization_header(client):
    origin = "http://localhost:3000"
    response = client.options(
        "/api/auth/me",
        headers={
            "Origin": origin,
            "Access-Control-Request-Method": "GET",
            "Access-Control-Request-Headers": "Authorization",
        },
    )
    assert response.headers["Access-Control-Allow-Origin"] == origin
    assert "Authorization" in response.headers["Access-Control-Allow-Headers"]


def test_protected_route_still_returns_401_with_json_error(client):
    response = client.get("/api/auth/me")
    assert response.status_code == 401
    assert "error" in response.get_json()
