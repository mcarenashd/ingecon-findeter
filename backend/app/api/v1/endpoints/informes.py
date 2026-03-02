from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.contrato import ContratoObra
from app.models.informe import (
    EstadoInforme,
    InformeFoto,
    InformeSemanal,
    SnapshotHito,
)
from app.schemas.foto import InformeFotoCreate, InformeFotoResponse, InformeFotoUpdate
from app.schemas.informe import (
    InformeGenerarRequest,
    InformeSemanalDetailResponse,
    InformeSemanalListResponse,
    InformeSemanalResponse,
    InformeSemanalUpdate,
    InformeSemanalUpdateS3,
    InformeSemanalUpdateS5,
    InformeSemanalUpdateS6Ambiental,
    InformeSemanalUpdateS6Social,
    InformeSemanalUpdateS6SST,
    InformeSemanalUpdateS6Tecnico,
    InformeTransicionEstado,
    SnapshotHitoResponse,
)
from app.services.informe_generator import generate_informe_semanal, refresh_hitos_snapshot

router = APIRouter(prefix="/informes", tags=["Informes"])


# --- Helpers ---


def _get_informe_or_404(informe_id: int, db: Session) -> InformeSemanal:
    informe = db.get(InformeSemanal, informe_id)
    if not informe:
        raise HTTPException(status_code=404, detail="Informe semanal no encontrado")
    return informe


def _require_borrador(informe: InformeSemanal) -> None:
    if informe.estado != EstadoInforme.BORRADOR:
        raise HTTPException(
            status_code=400,
            detail="Solo se puede editar un informe en estado BORRADOR",
        )


# --- Generación ---


@router.post(
    "/semanales/generar",
    response_model=InformeSemanalDetailResponse,
    status_code=status.HTTP_201_CREATED,
)
def generar_informe(data: InformeGenerarRequest, db: Session = Depends(get_db)):
    contrato = db.get(ContratoObra, data.contrato_obra_id)
    if not contrato:
        raise HTTPException(status_code=404, detail="Contrato de obra no encontrado")
    try:
        informe = generate_informe_semanal(
            db=db,
            contrato_obra_id=data.contrato_obra_id,
            semana_inicio=data.semana_inicio,
            semana_fin=data.semana_fin,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return informe


@router.post(
    "/semanales/generar-todos",
    response_model=list[InformeSemanalListResponse],
    status_code=status.HTTP_201_CREATED,
)
def generar_todos_informes(
    semana_inicio: str,
    semana_fin: str,
    db: Session = Depends(get_db),
):
    from datetime import date

    inicio = date.fromisoformat(semana_inicio)
    fin = date.fromisoformat(semana_fin)

    contratos = db.query(ContratoObra).all()
    informes_creados = []
    for contrato in contratos:
        try:
            informe = generate_informe_semanal(
                db=db,
                contrato_obra_id=contrato.id,
                semana_inicio=inicio,
                semana_fin=fin,
            )
            informes_creados.append(informe)
        except ValueError:
            continue  # Ya existe para este contrato/semana
    return informes_creados


# --- CRUD ---


@router.get("/semanales", response_model=list[InformeSemanalListResponse])
def listar_informes(
    contrato_obra_id: int | None = None,
    estado: EstadoInforme | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(InformeSemanal)
    if contrato_obra_id:
        query = query.filter(InformeSemanal.contrato_obra_id == contrato_obra_id)
    if estado:
        query = query.filter(InformeSemanal.estado == estado)
    return query.order_by(InformeSemanal.numero_informe.desc()).all()


@router.get("/semanales/{informe_id}", response_model=InformeSemanalDetailResponse)
def obtener_informe(informe_id: int, db: Session = Depends(get_db)):
    return _get_informe_or_404(informe_id, db)


@router.patch("/semanales/{informe_id}", response_model=InformeSemanalResponse)
def actualizar_informe(
    informe_id: int, data: InformeSemanalUpdate, db: Session = Depends(get_db)
):
    informe = _get_informe_or_404(informe_id, db)
    _require_borrador(informe)
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(informe, field, value)
    db.commit()
    db.refresh(informe)
    return informe


# --- Edición por sección ---


@router.patch(
    "/semanales/{informe_id}/seccion/s3", response_model=InformeSemanalResponse
)
def actualizar_seccion_s3(
    informe_id: int, data: InformeSemanalUpdateS3, db: Session = Depends(get_db)
):
    informe = _get_informe_or_404(informe_id, db)
    _require_borrador(informe)
    informe.situaciones_problematicas = data.situaciones_problematicas
    db.commit()
    db.refresh(informe)
    return informe


@router.patch(
    "/semanales/{informe_id}/seccion/s5", response_model=InformeSemanalResponse
)
def actualizar_seccion_s5(
    informe_id: int, data: InformeSemanalUpdateS5, db: Session = Depends(get_db)
):
    informe = _get_informe_or_404(informe_id, db)
    _require_borrador(informe)
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(informe, field, value)
    db.commit()
    db.refresh(informe)
    return informe


@router.patch(
    "/semanales/{informe_id}/seccion/s6-tecnico",
    response_model=InformeSemanalResponse,
)
def actualizar_seccion_s6_tecnico(
    informe_id: int, data: InformeSemanalUpdateS6Tecnico, db: Session = Depends(get_db)
):
    informe = _get_informe_or_404(informe_id, db)
    _require_borrador(informe)
    informe.comentario_tecnico = data.comentario_tecnico
    db.commit()
    db.refresh(informe)
    return informe


@router.patch(
    "/semanales/{informe_id}/seccion/s6-sst",
    response_model=InformeSemanalResponse,
)
def actualizar_seccion_s6_sst(
    informe_id: int, data: InformeSemanalUpdateS6SST, db: Session = Depends(get_db)
):
    informe = _get_informe_or_404(informe_id, db)
    _require_borrador(informe)
    informe.comentario_sst = data.comentario_sst
    db.commit()
    db.refresh(informe)
    return informe


@router.patch(
    "/semanales/{informe_id}/seccion/s6-ambiental",
    response_model=InformeSemanalResponse,
)
def actualizar_seccion_s6_ambiental(
    informe_id: int,
    data: InformeSemanalUpdateS6Ambiental,
    db: Session = Depends(get_db),
):
    informe = _get_informe_or_404(informe_id, db)
    _require_borrador(informe)
    informe.comentario_ambiental = data.comentario_ambiental
    db.commit()
    db.refresh(informe)
    return informe


@router.patch(
    "/semanales/{informe_id}/seccion/s6-social",
    response_model=InformeSemanalResponse,
)
def actualizar_seccion_s6_social(
    informe_id: int,
    data: InformeSemanalUpdateS6Social,
    db: Session = Depends(get_db),
):
    informe = _get_informe_or_404(informe_id, db)
    _require_borrador(informe)
    informe.comentario_social = data.comentario_social
    db.commit()
    db.refresh(informe)
    return informe


# --- Transiciones de estado ---


TRANSICIONES_VALIDAS = {
    EstadoInforme.BORRADOR: [EstadoInforme.EN_REVISION],
    EstadoInforme.EN_REVISION: [EstadoInforme.BORRADOR, EstadoInforme.APROBADO],
    EstadoInforme.APROBADO: [EstadoInforme.RADICADO],
    EstadoInforme.RADICADO: [],
}


@router.post(
    "/semanales/{informe_id}/transicion",
    response_model=InformeSemanalResponse,
)
def transicion_estado(
    informe_id: int,
    data: InformeTransicionEstado,
    db: Session = Depends(get_db),
):
    informe = _get_informe_or_404(informe_id, db)

    estados_permitidos = TRANSICIONES_VALIDAS.get(informe.estado, [])
    if data.nuevo_estado not in estados_permitidos:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Transición no permitida: {informe.estado.value} → "
                f"{data.nuevo_estado.value}. "
                f"Transiciones válidas: {[e.value for e in estados_permitidos]}"
            ),
        )

    now = datetime.now(timezone.utc)
    informe.estado = data.nuevo_estado

    if data.nuevo_estado == EstadoInforme.EN_REVISION:
        informe.fecha_envio_revision = now
    elif data.nuevo_estado == EstadoInforme.APROBADO:
        informe.fecha_aprobacion = now
    elif data.nuevo_estado == EstadoInforme.RADICADO:
        informe.fecha_radicacion = now

    db.commit()
    db.refresh(informe)
    return informe


# --- Snapshots de hitos ---


@router.get(
    "/semanales/{informe_id}/snapshot-hitos",
    response_model=list[SnapshotHitoResponse],
)
def listar_snapshot_hitos(informe_id: int, db: Session = Depends(get_db)):
    informe = _get_informe_or_404(informe_id, db)
    return (
        db.query(SnapshotHito)
        .filter(SnapshotHito.informe_semanal_id == informe.id)
        .order_by(SnapshotHito.numero)
        .all()
    )


@router.post(
    "/semanales/{informe_id}/refresh-snapshot",
    response_model=list[SnapshotHitoResponse],
)
def refrescar_snapshot(informe_id: int, db: Session = Depends(get_db)):
    informe = _get_informe_or_404(informe_id, db)
    try:
        snapshots = refresh_hitos_snapshot(db, informe)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return snapshots


# --- Fotos del informe (S7) ---


@router.get(
    "/semanales/{informe_id}/fotos",
    response_model=list[InformeFotoResponse],
)
def listar_fotos_informe(informe_id: int, db: Session = Depends(get_db)):
    _get_informe_or_404(informe_id, db)
    return (
        db.query(InformeFoto)
        .filter(InformeFoto.informe_semanal_id == informe_id)
        .order_by(InformeFoto.orden)
        .all()
    )


@router.post(
    "/semanales/{informe_id}/fotos",
    response_model=InformeFotoResponse,
    status_code=status.HTTP_201_CREATED,
)
def agregar_foto_informe(
    informe_id: int, data: InformeFotoCreate, db: Session = Depends(get_db)
):
    informe = _get_informe_or_404(informe_id, db)
    _require_borrador(informe)

    from app.models.foto import Foto

    foto = db.get(Foto, data.foto_id)
    if not foto:
        raise HTTPException(status_code=404, detail="Foto no encontrada")

    informe_foto = InformeFoto(
        informe_semanal_id=informe_id,
        **data.model_dump(),
    )
    db.add(informe_foto)
    db.commit()
    db.refresh(informe_foto)
    return informe_foto


@router.patch(
    "/semanales/{informe_id}/fotos/{informe_foto_id}",
    response_model=InformeFotoResponse,
)
def actualizar_foto_informe(
    informe_id: int,
    informe_foto_id: int,
    data: InformeFotoUpdate,
    db: Session = Depends(get_db),
):
    informe = _get_informe_or_404(informe_id, db)
    _require_borrador(informe)

    informe_foto = db.get(InformeFoto, informe_foto_id)
    if not informe_foto or informe_foto.informe_semanal_id != informe_id:
        raise HTTPException(status_code=404, detail="Foto del informe no encontrada")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(informe_foto, field, value)
    db.commit()
    db.refresh(informe_foto)
    return informe_foto


@router.delete(
    "/semanales/{informe_id}/fotos/{informe_foto_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def eliminar_foto_informe(
    informe_id: int, informe_foto_id: int, db: Session = Depends(get_db)
):
    informe = _get_informe_or_404(informe_id, db)
    _require_borrador(informe)

    informe_foto = db.get(InformeFoto, informe_foto_id)
    if not informe_foto or informe_foto.informe_semanal_id != informe_id:
        raise HTTPException(status_code=404, detail="Foto del informe no encontrada")

    db.delete(informe_foto)
    db.commit()
