from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.contrato import ContratoObra
from app.models.informe import InformeSemanal
from app.schemas.informe import (
    InformeSemanalCreate,
    InformeSemanalResponse,
    InformeSemanalUpdate,
)

router = APIRouter(prefix="/informes", tags=["Informes"])


@router.get("/semanales", response_model=list[InformeSemanalResponse])
def listar_informes(
    contrato_obra_id: int | None = None, db: Session = Depends(get_db)
):
    query = db.query(InformeSemanal)
    if contrato_obra_id:
        query = query.filter(InformeSemanal.contrato_obra_id == contrato_obra_id)
    return query.order_by(InformeSemanal.numero_informe.desc()).all()


@router.post(
    "/semanales",
    response_model=InformeSemanalResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_informe(data: InformeSemanalCreate, db: Session = Depends(get_db)):
    contrato = db.get(ContratoObra, data.contrato_obra_id)
    if not contrato:
        raise HTTPException(status_code=404, detail="Contrato de obra no encontrado")
    informe = InformeSemanal(**data.model_dump())
    db.add(informe)
    db.commit()
    db.refresh(informe)
    return informe


@router.get("/semanales/{informe_id}", response_model=InformeSemanalResponse)
def obtener_informe(informe_id: int, db: Session = Depends(get_db)):
    informe = db.get(InformeSemanal, informe_id)
    if not informe:
        raise HTTPException(status_code=404, detail="Informe semanal no encontrado")
    return informe


@router.patch("/semanales/{informe_id}", response_model=InformeSemanalResponse)
def actualizar_informe(
    informe_id: int, data: InformeSemanalUpdate, db: Session = Depends(get_db)
):
    informe = db.get(InformeSemanal, informe_id)
    if not informe:
        raise HTTPException(status_code=404, detail="Informe semanal no encontrado")
    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(informe, field, value)
    db.commit()
    db.refresh(informe)
    return informe
