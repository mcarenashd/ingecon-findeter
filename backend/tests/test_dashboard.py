"""Tests for dashboard endpoint."""

from datetime import date
from decimal import Decimal

from app.models.contrato import ContratoInterventoria, ContratoObra, Hito
from tests.conftest import auth_header


def test_dashboard_empty(client, director_token, director_user):
    res = client.get("/api/v1/dashboard", headers=auth_header(director_token))
    assert res.status_code == 200
    data = res.json()
    assert data["total_contratos_obra"] == 0
    assert data["total_informes_pendientes"] == 0


def test_dashboard_with_data(client, director_token, director_user, db):
    # Create interventoria contract
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

    # Create obra contract
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

    res = client.get("/api/v1/dashboard", headers=auth_header(director_token))
    assert res.status_code == 200
    data = res.json()
    assert data["total_contratos_obra"] == 1
    assert data["valor_total_obra"] == "500000000.00"


def test_health_check(client):
    res = client.get("/health")
    assert res.status_code == 200
    assert res.json()["status"] == "ok"
