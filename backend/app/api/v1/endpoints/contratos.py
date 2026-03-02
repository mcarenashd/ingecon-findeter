from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.contrato import (
    ActividadNoPrevista,
    ContratoInterventoria,
    ContratoObra,
    Hito,
)
from app.schemas.actividad_no_prevista import (
    ActividadNoPrevistaCreate,
    ActividadNoPrevistaResponse,
    ActividadNoPrevistaUpdate,
)
from app.schemas.contrato import (
    ContratoInterventoriaCreate,
    ContratoInterventoriaResponse,
    ContratoObraCreate,
    ContratoObraResponse,
    HitoCreate,
    HitoResponse,
)

router = APIRouter(prefix="/contratos", tags=["Contratos"])


# --- Contrato Interventoría ---


@router.get("/interventoria", response_model=list[ContratoInterventoriaResponse])
def listar_contratos_interventoria(db: Session = Depends(get_db)):
    return db.query(ContratoInterventoria).all()


@router.post(
    "/interventoria",
    response_model=ContratoInterventoriaResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_contrato_interventoria(
    data: ContratoInterventoriaCreate, db: Session = Depends(get_db)
):
    contrato = ContratoInterventoria(**data.model_dump())
    db.add(contrato)
    db.commit()
    db.refresh(contrato)
    return contrato


@router.get("/interventoria/{contrato_id}", response_model=ContratoInterventoriaResponse)
def obtener_contrato_interventoria(contrato_id: int, db: Session = Depends(get_db)):
    contrato = db.get(ContratoInterventoria, contrato_id)
    if not contrato:
        raise HTTPException(status_code=404, detail="Contrato de interventoría no encontrado")
    return contrato


# --- Contratos de Obra ---


@router.get("/obra", response_model=list[ContratoObraResponse])
def listar_contratos_obra(db: Session = Depends(get_db)):
    return db.query(ContratoObra).all()


@router.post(
    "/obra",
    response_model=ContratoObraResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_contrato_obra(data: ContratoObraCreate, db: Session = Depends(get_db)):
    # Verificar que el contrato de interventoría existe
    interventoria = db.get(ContratoInterventoria, data.contrato_interventoria_id)
    if not interventoria:
        raise HTTPException(status_code=404, detail="Contrato de interventoría no encontrado")
    contrato = ContratoObra(**data.model_dump())
    db.add(contrato)
    db.commit()
    db.refresh(contrato)
    return contrato


@router.get("/obra/{contrato_id}", response_model=ContratoObraResponse)
def obtener_contrato_obra(contrato_id: int, db: Session = Depends(get_db)):
    contrato = db.get(ContratoObra, contrato_id)
    if not contrato:
        raise HTTPException(status_code=404, detail="Contrato de obra no encontrado")
    return contrato


# --- Hitos ---


@router.get("/obra/{contrato_id}/hitos", response_model=list[HitoResponse])
def listar_hitos(contrato_id: int, db: Session = Depends(get_db)):
    contrato = db.get(ContratoObra, contrato_id)
    if not contrato:
        raise HTTPException(status_code=404, detail="Contrato de obra no encontrado")
    return db.query(Hito).filter(Hito.contrato_obra_id == contrato_id).all()


@router.post(
    "/obra/{contrato_id}/hitos",
    response_model=HitoResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_hito(contrato_id: int, data: HitoCreate, db: Session = Depends(get_db)):
    contrato = db.get(ContratoObra, contrato_id)
    if not contrato:
        raise HTTPException(status_code=404, detail="Contrato de obra no encontrado")
    hito = Hito(**data.model_dump())
    hito.contrato_obra_id = contrato_id
    db.add(hito)
    db.commit()
    db.refresh(hito)
    return hito


# --- Actividades No Previstas ---


@router.get(
    "/obra/{contrato_id}/actividades-no-previstas",
    response_model=list[ActividadNoPrevistaResponse],
)
def listar_actividades_no_previstas(contrato_id: int, db: Session = Depends(get_db)):
    contrato = db.get(ContratoObra, contrato_id)
    if not contrato:
        raise HTTPException(status_code=404, detail="Contrato de obra no encontrado")
    return (
        db.query(ActividadNoPrevista)
        .filter(ActividadNoPrevista.contrato_obra_id == contrato_id)
        .order_by(ActividadNoPrevista.codigo)
        .all()
    )


@router.post(
    "/obra/{contrato_id}/actividades-no-previstas",
    response_model=ActividadNoPrevistaResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_actividad_no_prevista(
    contrato_id: int, data: ActividadNoPrevistaCreate, db: Session = Depends(get_db)
):
    contrato = db.get(ContratoObra, contrato_id)
    if not contrato:
        raise HTTPException(status_code=404, detail="Contrato de obra no encontrado")
    actividad = ActividadNoPrevista(
        contrato_obra_id=contrato_id,
        **data.model_dump(),
    )
    db.add(actividad)
    db.commit()
    db.refresh(actividad)
    return actividad


@router.patch(
    "/obra/{contrato_id}/actividades-no-previstas/{actividad_id}",
    response_model=ActividadNoPrevistaResponse,
)
def actualizar_actividad_no_prevista(
    contrato_id: int,
    actividad_id: int,
    data: ActividadNoPrevistaUpdate,
    db: Session = Depends(get_db),
):
    actividad = db.get(ActividadNoPrevista, actividad_id)
    if not actividad or actividad.contrato_obra_id != contrato_id:
        raise HTTPException(status_code=404, detail="Actividad no prevista no encontrada")
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(actividad, field, value)
    db.commit()
    db.refresh(actividad)
    return actividad
