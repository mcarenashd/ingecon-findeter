"""Tests for usuarios CRUD endpoints."""

from tests.conftest import auth_header


def test_listar_usuarios(client, director_token, director_user):
    res = client.get("/api/v1/usuarios", headers=auth_header(director_token))
    assert res.status_code == 200
    data = res.json()
    assert len(data) == 1
    assert data[0]["email"] == "director@test.co"


def test_listar_usuarios_tecnico(client, tecnico_token, tecnico_user, director_user):
    """Any authenticated user can list users."""
    res = client.get("/api/v1/usuarios", headers=auth_header(tecnico_token))
    assert res.status_code == 200
    assert len(res.json()) == 2


def test_crear_usuario_director(client, director_token, director_user):
    res = client.post(
        "/api/v1/usuarios",
        headers=auth_header(director_token),
        json={
            "email": "nuevo@test.co",
            "nombre_completo": "Nuevo Usuario",
            "rol": "residente_sst",
            "password": "Pass1234",
        },
    )
    assert res.status_code == 201
    data = res.json()
    assert data["email"] == "nuevo@test.co"
    assert data["rol"] == "residente_sst"
    assert data["activo"] is True
    assert "hashed_password" not in data


def test_crear_usuario_email_duplicado(client, director_token, director_user):
    res = client.post(
        "/api/v1/usuarios",
        headers=auth_header(director_token),
        json={
            "email": "director@test.co",
            "nombre_completo": "Otro Director",
            "rol": "supervisor",
            "password": "Pass1234",
        },
    )
    assert res.status_code == 400
    assert "email" in res.json()["detail"].lower()


def test_crear_usuario_sin_permisos(client, tecnico_token, tecnico_user):
    """Only directors can create users."""
    res = client.post(
        "/api/v1/usuarios",
        headers=auth_header(tecnico_token),
        json={
            "email": "otro@test.co",
            "nombre_completo": "Otro",
            "rol": "residente_sst",
            "password": "Pass1234",
        },
    )
    assert res.status_code == 403


def test_obtener_usuario(client, director_token, director_user):
    res = client.get(
        f"/api/v1/usuarios/{director_user.id}",
        headers=auth_header(director_token),
    )
    assert res.status_code == 200
    assert res.json()["email"] == "director@test.co"


def test_obtener_usuario_no_existe(client, director_token, director_user):
    res = client.get("/api/v1/usuarios/999", headers=auth_header(director_token))
    assert res.status_code == 404


def test_editar_usuario(client, director_token, director_user, tecnico_user):
    res = client.patch(
        f"/api/v1/usuarios/{tecnico_user.id}",
        headers=auth_header(director_token),
        json={"nombre_completo": "Nuevo Nombre"},
    )
    assert res.status_code == 200
    assert res.json()["nombre_completo"] == "Nuevo Nombre"


def test_desactivar_usuario(client, director_token, director_user, tecnico_user):
    res = client.patch(
        f"/api/v1/usuarios/{tecnico_user.id}",
        headers=auth_header(director_token),
        json={"activo": False},
    )
    assert res.status_code == 200
    assert res.json()["activo"] is False


def test_cambiar_password(client, director_token, director_user, tecnico_user):
    # Change password
    res = client.patch(
        f"/api/v1/usuarios/{tecnico_user.id}",
        headers=auth_header(director_token),
        json={"password": "NuevoPass123"},
    )
    assert res.status_code == 200

    # Login with new password
    res2 = client.post(
        "/api/v1/auth/login",
        data={"username": "tecnico@test.co", "password": "NuevoPass123"},
    )
    assert res2.status_code == 200


def test_editar_usuario_sin_permisos(client, tecnico_token, tecnico_user, director_user):
    res = client.patch(
        f"/api/v1/usuarios/{director_user.id}",
        headers=auth_header(tecnico_token),
        json={"nombre_completo": "Hacked"},
    )
    assert res.status_code == 403
