"""Tests for authentication endpoints."""

from tests.conftest import auth_header


def test_login_success(client, director_user):
    res = client.post(
        "/api/v1/auth/login",
        data={"username": "director@test.co", "password": "Test1234"},
    )
    assert res.status_code == 200
    data = res.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"


def test_login_wrong_password(client, director_user):
    res = client.post(
        "/api/v1/auth/login",
        data={"username": "director@test.co", "password": "WrongPass"},
    )
    assert res.status_code == 401
    assert res.json()["detail"] == "Credenciales incorrectas"


def test_login_nonexistent_user(client):
    res = client.post(
        "/api/v1/auth/login",
        data={"username": "noexiste@test.co", "password": "Test1234"},
    )
    assert res.status_code == 401


def test_login_inactive_user(client, db, director_user):
    director_user.activo = False
    db.commit()
    res = client.post(
        "/api/v1/auth/login",
        data={"username": "director@test.co", "password": "Test1234"},
    )
    assert res.status_code == 403
    assert res.json()["detail"] == "Usuario inactivo"


def test_protected_endpoint_no_token(client):
    res = client.get("/api/v1/usuarios")
    assert res.status_code == 401


def test_protected_endpoint_invalid_token(client):
    res = client.get("/api/v1/usuarios", headers=auth_header("invalid.token.here"))
    assert res.status_code == 401


def test_protected_endpoint_valid_token(client, director_token):
    res = client.get("/api/v1/usuarios", headers=auth_header(director_token))
    assert res.status_code == 200
