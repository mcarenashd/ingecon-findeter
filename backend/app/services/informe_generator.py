from datetime import date, datetime, timezone
from decimal import Decimal

from sqlalchemy import and_
from sqlalchemy.orm import Session

from app.models.contrato import ContratoObra, Hito
from app.models.foto import Foto
from app.models.informe import (
    AccionPlan,
    EstadoInforme,
    EstadoPlanAccion,
    InformeFoto,
    InformeSemanal,
    SnapshotHito,
)


def generate_informe_semanal(
    db: Session,
    contrato_obra_id: int,
    semana_inicio: date,
    semana_fin: date,
    creado_por_id: int | None = None,
) -> InformeSemanal:
    """Genera un borrador de informe semanal con datos pre-llenados.

    1. Crea el InformeSemanal con numero_informe auto-calculado
    2. Toma snapshot de todos los hitos del contrato
    3. Calcula indicadores S2
    4. Marca acciones vencidas de informes anteriores
    5. Pre-carga fotos de la semana
    """
    contrato = db.get(ContratoObra, contrato_obra_id)
    if not contrato:
        raise ValueError(f"Contrato de obra {contrato_obra_id} no encontrado")

    # Verificar que no exista un informe para esta semana/contrato
    existente = (
        db.query(InformeSemanal)
        .filter(
            InformeSemanal.contrato_obra_id == contrato_obra_id,
            InformeSemanal.semana_inicio == semana_inicio,
            InformeSemanal.semana_fin == semana_fin,
        )
        .first()
    )
    if existente:
        raise ValueError(
            f"Ya existe un informe para el contrato {contrato_obra_id} "
            f"en la semana {semana_inicio} - {semana_fin}"
        )

    # Calcular numero_informe
    count = (
        db.query(InformeSemanal)
        .filter(InformeSemanal.contrato_obra_id == contrato_obra_id)
        .count()
    )
    numero_informe = count + 1

    # Crear informe
    informe = InformeSemanal(
        contrato_obra_id=contrato_obra_id,
        numero_informe=numero_informe,
        semana_inicio=semana_inicio,
        semana_fin=semana_fin,
        estado=EstadoInforme.BORRADOR,
        creado_por_id=creado_por_id,
    )
    db.add(informe)
    db.flush()  # Obtener informe.id

    # Snapshot de hitos (S2)
    _create_hitos_snapshot(db, informe)

    # Calcular indicadores S2
    _compute_indicators(db, informe)

    # Marcar acciones vencidas de informes anteriores
    _mark_overdue_actions(db, contrato_obra_id, semana_fin)

    # Pre-cargar fotos de la semana (S7)
    _preload_week_photos(db, informe, semana_inicio, semana_fin)

    db.commit()
    db.refresh(informe)
    return informe


def refresh_hitos_snapshot(db: Session, informe: InformeSemanal) -> list[SnapshotHito]:
    """Borra y recrea el snapshot de hitos. Solo para informes en BORRADOR."""
    if informe.estado != EstadoInforme.BORRADOR:
        raise ValueError("Solo se puede refrescar el snapshot en estado BORRADOR")

    # Borrar snapshots existentes
    db.query(SnapshotHito).filter(
        SnapshotHito.informe_semanal_id == informe.id
    ).delete()

    _create_hitos_snapshot(db, informe)
    _compute_indicators(db, informe)

    db.commit()
    db.refresh(informe)
    return informe.snapshot_hitos


def _create_hitos_snapshot(db: Session, informe: InformeSemanal) -> None:
    """Copia el estado actual de cada hito del contrato al snapshot."""
    hitos = (
        db.query(Hito)
        .filter(Hito.contrato_obra_id == informe.contrato_obra_id)
        .order_by(Hito.numero)
        .all()
    )

    for hito in hitos:
        snapshot = SnapshotHito(
            informe_semanal_id=informe.id,
            hito_id=hito.id,
            numero=hito.numero,
            descripcion=hito.descripcion,
            fecha_programada=hito.fecha_programada,
            fecha_real=hito.fecha_real,
            estado=hito.estado,
            avance_porcentaje=hito.avance_porcentaje,
            dias_retraso=hito.dias_retraso,
        )
        db.add(snapshot)


def _compute_indicators(db: Session, informe: InformeSemanal) -> None:
    """Calcula los indicadores de avance físico y financiero (S2)."""
    hitos = (
        db.query(Hito)
        .filter(Hito.contrato_obra_id == informe.contrato_obra_id)
        .all()
    )

    if not hitos:
        return

    # Avance físico ejecutado = promedio ponderado de avance de hitos
    total_avance = sum(h.avance_porcentaje for h in hitos)
    informe.avance_fisico_ejecutado = Decimal(str(total_avance / len(hitos)))

    # Avance programado: ratio de hitos cuya fecha programada ya pasó
    today = date.today()
    hitos_vencidos = sum(1 for h in hitos if h.fecha_programada <= today)
    informe.avance_fisico_programado = Decimal(
        str(round(hitos_vencidos / len(hitos) * 100, 2))
    )

    # Valores acumulados del contrato
    contrato = db.get(ContratoObra, informe.contrato_obra_id)
    if contrato:
        informe.valor_acumulado_programado = contrato.valor_actualizado * (
            informe.avance_fisico_programado / Decimal("100")
        )
        informe.valor_acumulado_ejecutado = contrato.valor_actualizado * (
            informe.avance_fisico_ejecutado / Decimal("100")
        )


def _mark_overdue_actions(
    db: Session, contrato_obra_id: int, fecha_corte: date
) -> None:
    """Marca como VENCIDO las acciones PENDIENTE cuya fecha_programada ya pasó."""
    informe_ids = (
        db.query(InformeSemanal.id)
        .filter(InformeSemanal.contrato_obra_id == contrato_obra_id)
        .subquery()
    )

    db.query(AccionPlan).filter(
        AccionPlan.informe_origen_id.in_(informe_ids),
        AccionPlan.estado == EstadoPlanAccion.PENDIENTE,
        AccionPlan.fecha_programada < fecha_corte,
    ).update(
        {AccionPlan.estado: EstadoPlanAccion.VENCIDO},
        synchronize_session="fetch",
    )


def _preload_week_photos(
    db: Session,
    informe: InformeSemanal,
    semana_inicio: date,
    semana_fin: date,
) -> None:
    """Pre-carga las fotos subidas durante la semana como fotos del informe."""
    fotos = (
        db.query(Foto)
        .filter(
            Foto.contrato_obra_id == informe.contrato_obra_id,
            and_(Foto.fecha_toma >= semana_inicio, Foto.fecha_toma <= semana_fin),
        )
        .order_by(Foto.fecha_toma, Foto.id)
        .all()
    )

    for idx, foto in enumerate(fotos):
        informe_foto = InformeFoto(
            informe_semanal_id=informe.id,
            foto_id=foto.id,
            orden=idx + 1,
        )
        db.add(informe_foto)
