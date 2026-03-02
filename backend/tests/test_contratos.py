"""Tests for contratos and hitos endpoints."""

from datetime import date
from decimal import Decimal

from app.models.contrato import ContratoInterventoria, ContratoObra
from tests.conftest import auth_header


def _create_contrato(db) -> ContratoObra:
    """Helper to create a full contract chain."""
    interv = ContratoInterventoria(
        numero="INT-001",
        objeto="Interventoría test",
        valor_inicial=Decimal("100000000"),
        valor_actualizado=Decimal("100000000"),
        plazo_dias=180,
        fecha_inicio=date(2025, 1, 1),
        fecha_terminacion=date(2025, 6, 30),
        contratista="Test Interv",
        supervisor="Test Supervisor",
    )
    db.add(interv)
    db.flush()

    obra = ContratoObra(
        contrato_interventoria_id=interv.id,
        numero="CTO-001",
        objeto="Obra test",
        contratista="Constructor Test",
        valor_inicial=Decimal("500000000"),
        adiciones=Decimal("0"),
        valor_actualizado=Decimal("500000000"),
        plazo_dias=360,
        fecha_inicio=date(2025, 1, 1),
        fecha_terminacion=date(2025, 12, 31),
    )
    db.add(obra)
    db.commit()
    db.refresh(obra)
    return obra


# --- Contratos Interventoría ---


def test_listar_contratos_interventoria(client, director_token, director_user, db):
    _create_contrato(db)
    res = client.get(
        "/api/v1/contratos/interventoria",
        headers=auth_header(director_token),
    )
    assert res.status_code == 200
    assert len(res.json()) == 1


def test_crear_contrato_interventoria(client, director_token, director_user):
    res = client.post(
        "/api/v1/contratos/interventoria",
        headers=auth_header(director_token),
        json={
            "numero": "INT-NEW",
            "objeto": "Nueva interventoría",
            "valor_inicial": "200000000",
            "valor_actualizado": "200000000",
            "plazo_dias": 365,
            "fecha_inicio": "2025-01-01",
            "fecha_terminacion": "2025-12-31",
            "contratista": "Test",
            "supervisor": "Supervisor",
        },
    )
    assert res.status_code == 201
    assert res.json()["numero"] == "INT-NEW"


# --- Contratos Obra ---


def test_listar_contratos_obra(client, director_token, director_user, db):
    _create_contrato(db)
    res = client.get("/api/v1/contratos/obra", headers=auth_header(director_token))
    assert res.status_code == 200
    assert len(res.json()) == 1
    assert res.json()[0]["numero"] == "CTO-001"


def test_obtener_contrato_obra(client, director_token, director_user, db):
    obra = _create_contrato(db)
    res = client.get(
        f"/api/v1/contratos/obra/{obra.id}",
        headers=auth_header(director_token),
    )
    assert res.status_code == 200
    assert res.json()["contratista"] == "Constructor Test"


def test_contrato_obra_no_existe(client, director_token, director_user):
    res = client.get("/api/v1/contratos/obra/999", headers=auth_header(director_token))
    assert res.status_code == 404


# --- Hitos ---


def test_crear_hito(client, director_token, director_user, db):
    obra = _create_contrato(db)
    res = client.post(
        f"/api/v1/contratos/obra/{obra.id}/hitos",
        headers=auth_header(director_token),
        json={
            "contrato_obra_id": obra.id,
            "numero": 1,
            "descripcion": "Hito de prueba",
            "fecha_programada": "2025-03-15",
        },
    )
    assert res.status_code == 201
    assert res.json()["descripcion"] == "Hito de prueba"


def test_listar_hitos(client, director_token, director_user, db):
    obra = _create_contrato(db)
    # Create 2 hitos
    for i in range(1, 3):
        client.post(
            f"/api/v1/contratos/obra/{obra.id}/hitos",
            headers=auth_header(director_token),
            json={
                "contrato_obra_id": obra.id,
                "numero": i,
                "descripcion": f"Hito {i}",
                "fecha_programada": f"2025-0{i}-15",
            },
        )

    res = client.get(
        f"/api/v1/contratos/obra/{obra.id}/hitos",
        headers=auth_header(director_token),
    )
    assert res.status_code == 200
    assert len(res.json()) == 2
