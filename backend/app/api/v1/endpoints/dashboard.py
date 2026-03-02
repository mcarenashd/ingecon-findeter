from datetime import date
from decimal import Decimal

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.contrato import ContratoObra, EstadoHito, Hito
from app.models.informe import InformeSemanal

router = APIRouter(prefix="/dashboard", tags=["Dashboard"])


class HitoResumen(BaseModel):
    id: int
    contrato_numero: str
    descripcion: str
    fecha_programada: date
    dias_retraso: int
    estado: EstadoHito
    avance_porcentaje: Decimal

    model_config = {"from_attributes": True}


class DashboardResponse(BaseModel):
    total_contratos_obra: int
    valor_total_obra: Decimal
    hitos_en_retraso: list[HitoResumen]
    total_informes_pendientes: int
    avance_fisico_general: Decimal


@router.get("", response_model=DashboardResponse)
def obtener_dashboard(db: Session = Depends(get_db)):
    contratos = db.query(ContratoObra).all()
    total_valor = sum(c.valor_actualizado for c in contratos) if contratos else Decimal("0")

    hitos_retrasados = (
        db.query(Hito)
        .filter(Hito.estado.in_([EstadoHito.VENCIDO, EstadoHito.EN_PROCESO]))
        .all()
    )
    hitos_resumen = []
    for h in hitos_retrasados:
        if h.dias_retraso > 0:
            hitos_resumen.append(
                HitoResumen(
                    id=h.id,
                    contrato_numero=h.contrato_obra.numero,
                    descripcion=h.descripcion,
                    fecha_programada=h.fecha_programada,
                    dias_retraso=h.dias_retraso,
                    estado=h.estado,
                    avance_porcentaje=h.avance_porcentaje,
                )
            )

    informes_pendientes = (
        db.query(InformeSemanal)
        .filter(InformeSemanal.estado == "borrador")
        .count()
    )

    # Avance general promedio
    todos_hitos = db.query(Hito).all()
    if todos_hitos:
        avance = sum(h.avance_porcentaje for h in todos_hitos) / len(todos_hitos)
    else:
        avance = Decimal("0")

    return DashboardResponse(
        total_contratos_obra=len(contratos),
        valor_total_obra=total_valor,
        hitos_en_retraso=sorted(hitos_resumen, key=lambda h: h.dias_retraso, reverse=True),
        total_informes_pendientes=informes_pendientes,
        avance_fisico_general=avance,
    )
