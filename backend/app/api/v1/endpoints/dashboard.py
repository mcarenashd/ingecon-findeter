from datetime import date
from decimal import Decimal

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import func
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.contrato import ContratoObra, EstadoHito, Hito
from app.models.informe import EstadoInforme, InformeSemanal
from app.schemas.informe import CurvaSDataPoint, CurvaSResponse

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


@router.get("/curva-s", response_model=CurvaSResponse)
def obtener_curva_s_global(db: Session = Depends(get_db)):
    """Retorna la Curva S del contrato con más informes aprobados."""
    # Buscar el contrato con más informes no-borrador
    subq = (
        db.query(
            InformeSemanal.contrato_obra_id,
            func.count(InformeSemanal.id).label("cnt"),
        )
        .filter(InformeSemanal.estado != EstadoInforme.BORRADOR)
        .group_by(InformeSemanal.contrato_obra_id)
        .order_by(func.count(InformeSemanal.id).desc())
        .first()
    )

    if not subq:
        # Sin informes → retornar respuesta vacía con datos del primer contrato
        contrato = db.query(ContratoObra).first()
        return CurvaSResponse(
            contrato_obra_id=contrato.id if contrato else 0,
            contrato_numero=contrato.numero if contrato else "",
            datos=[],
        )

    contrato_id = subq[0]
    contrato = db.get(ContratoObra, contrato_id)

    informes = (
        db.query(InformeSemanal)
        .filter(
            InformeSemanal.contrato_obra_id == contrato_id,
            InformeSemanal.estado != EstadoInforme.BORRADOR,
        )
        .order_by(InformeSemanal.numero_informe)
        .all()
    )

    datos = [
        CurvaSDataPoint(
            semana=inf.numero_informe,
            semana_fin=inf.semana_fin,
            programado=inf.avance_fisico_programado,
            ejecutado=inf.avance_fisico_ejecutado,
        )
        for inf in informes
    ]

    return CurvaSResponse(
        contrato_obra_id=contrato.id,
        contrato_numero=contrato.numero,
        datos=datos,
    )
