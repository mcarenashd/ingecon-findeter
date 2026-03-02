"""Tests for informes endpoints (generate, export, curva-s)."""

from datetime import date
from decimal import Decimal

from app.models.contrato import ContratoInterventoria, ContratoObra, Hito
from tests.conftest import auth_header


def _setup_contrato_con_hitos(db) -> ContratoObra:
    """Create a contract with hitos for informe generation."""
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
    db.flush()

    # Add hitos
    for i in range(1, 4):
        db.add(Hito(
            contrato_obra_id=obra.id,
            numero=i,
            descripcion=f"Hito {i}",
            fecha_programada=date(2025, i * 2, 15),
        ))
    db.commit()
    db.refresh(obra)
    return obra


def test_generar_informe(client, director_token, director_user, db):
    obra = _setup_contrato_con_hitos(db)
    res = client.post(
        "/api/v1/informes/semanales/generar",
        headers=auth_header(director_token),
        json={
            "contrato_obra_id": obra.id,
            "semana_inicio": "2025-03-03",
            "semana_fin": "2025-03-09",
        },
    )
    assert res.status_code == 201
    data = res.json()
    assert data["numero_informe"] == 1
    assert data["estado"] == "borrador"
    assert len(data["snapshot_hitos"]) == 3


def test_listar_informes(client, director_token, director_user, db):
    obra = _setup_contrato_con_hitos(db)
    # Generate an informe first
    client.post(
        "/api/v1/informes/semanales/generar",
        headers=auth_header(director_token),
        json={
            "contrato_obra_id": obra.id,
            "semana_inicio": "2025-03-03",
            "semana_fin": "2025-03-09",
        },
    )

    res = client.get(
        f"/api/v1/informes/semanales?contrato_obra_id={obra.id}",
        headers=auth_header(director_token),
    )
    assert res.status_code == 200
    assert len(res.json()) == 1


def test_obtener_informe(client, director_token, director_user, db):
    obra = _setup_contrato_con_hitos(db)
    create_res = client.post(
        "/api/v1/informes/semanales/generar",
        headers=auth_header(director_token),
        json={
            "contrato_obra_id": obra.id,
            "semana_inicio": "2025-03-03",
            "semana_fin": "2025-03-09",
        },
    )
    informe_id = create_res.json()["id"]

    res = client.get(
        f"/api/v1/informes/semanales/{informe_id}",
        headers=auth_header(director_token),
    )
    assert res.status_code == 200
    assert res.json()["id"] == informe_id


def test_editar_seccion_s3(client, director_token, director_user, db):
    obra = _setup_contrato_con_hitos(db)
    create_res = client.post(
        "/api/v1/informes/semanales/generar",
        headers=auth_header(director_token),
        json={
            "contrato_obra_id": obra.id,
            "semana_inicio": "2025-03-03",
            "semana_fin": "2025-03-09",
        },
    )
    informe_id = create_res.json()["id"]

    res = client.patch(
        f"/api/v1/informes/semanales/{informe_id}/seccion/s3",
        headers=auth_header(director_token),
        json={"situaciones_problematicas": "Lluvia fuerte durante 3 días"},
    )
    assert res.status_code == 200
    assert res.json()["situaciones_problematicas"] == "Lluvia fuerte durante 3 días"


def test_transicion_estado(client, director_token, director_user, db):
    obra = _setup_contrato_con_hitos(db)
    create_res = client.post(
        "/api/v1/informes/semanales/generar",
        headers=auth_header(director_token),
        json={
            "contrato_obra_id": obra.id,
            "semana_inicio": "2025-03-03",
            "semana_fin": "2025-03-09",
        },
    )
    informe_id = create_res.json()["id"]

    # borrador → en_revision
    res = client.post(
        f"/api/v1/informes/semanales/{informe_id}/transicion",
        headers=auth_header(director_token),
        json={"nuevo_estado": "en_revision"},
    )
    assert res.status_code == 200
    assert res.json()["estado"] == "en_revision"


def test_transicion_invalida(client, director_token, director_user, db):
    obra = _setup_contrato_con_hitos(db)
    create_res = client.post(
        "/api/v1/informes/semanales/generar",
        headers=auth_header(director_token),
        json={
            "contrato_obra_id": obra.id,
            "semana_inicio": "2025-03-03",
            "semana_fin": "2025-03-09",
        },
    )
    informe_id = create_res.json()["id"]

    # borrador → aprobado (not allowed directly)
    res = client.post(
        f"/api/v1/informes/semanales/{informe_id}/transicion",
        headers=auth_header(director_token),
        json={"nuevo_estado": "aprobado"},
    )
    assert res.status_code == 400
    assert "no permitida" in res.json()["detail"].lower()


def test_exportar_excel(client, director_token, director_user, db):
    obra = _setup_contrato_con_hitos(db)
    create_res = client.post(
        "/api/v1/informes/semanales/generar",
        headers=auth_header(director_token),
        json={
            "contrato_obra_id": obra.id,
            "semana_inicio": "2025-03-03",
            "semana_fin": "2025-03-09",
        },
    )
    informe_id = create_res.json()["id"]

    res = client.get(
        f"/api/v1/informes/semanales/{informe_id}/exportar",
        headers=auth_header(director_token),
    )
    assert res.status_code == 200
    assert "spreadsheetml" in res.headers["content-type"]
    assert len(res.content) > 1000  # Valid xlsx file


def test_exportar_pdf(client, director_token, director_user, db):
    import shutil

    # Skip if LibreOffice is not installed
    if not shutil.which("soffice"):
        import pytest
        pytest.skip("LibreOffice not installed")

    obra = _setup_contrato_con_hitos(db)
    create_res = client.post(
        "/api/v1/informes/semanales/generar",
        headers=auth_header(director_token),
        json={
            "contrato_obra_id": obra.id,
            "semana_inicio": "2025-03-03",
            "semana_fin": "2025-03-09",
        },
    )
    informe_id = create_res.json()["id"]

    res = client.get(
        f"/api/v1/informes/semanales/{informe_id}/pdf",
        headers=auth_header(director_token),
    )
    assert res.status_code == 200
    assert res.headers["content-type"] == "application/pdf"
    assert len(res.content) > 5000  # Valid PDF file
    assert res.content[:5] == b"%PDF-"  # PDF magic bytes


def test_curva_s_por_contrato(client, director_token, director_user, db):
    obra = _setup_contrato_con_hitos(db)
    res = client.get(
        f"/api/v1/informes/semanales/curva-s/{obra.id}",
        headers=auth_header(director_token),
    )
    assert res.status_code == 200
    data = res.json()
    assert data["contrato_obra_id"] == obra.id
    assert data["contrato_numero"] == "CTO-001"
    assert data["datos"] == []  # No informes yet


def test_curva_s_contrato_no_existe(client, director_token, director_user):
    res = client.get(
        "/api/v1/informes/semanales/curva-s/999",
        headers=auth_header(director_token),
    )
    assert res.status_code == 404
