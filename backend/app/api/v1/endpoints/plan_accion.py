from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.models.informe import (
    AccionPlan,
    EstadoInforme,
    EstadoPlanAccion,
    InformeSemanal,
)
from app.schemas.plan_accion import AccionPlanCreate, AccionPlanResponse, AccionPlanUpdate

router = APIRouter(prefix="/informes/semanales/{informe_id}/plan-accion", tags=["Plan de Acción"])


def _get_informe_or_404(informe_id: int, db: Session) -> InformeSemanal:
    informe = db.get(InformeSemanal, informe_id)
    if not informe:
        raise HTTPException(status_code=404, detail="Informe semanal no encontrado")
    return informe


@router.get("", response_model=list[AccionPlanResponse])
def listar_acciones_plan(informe_id: int, db: Session = Depends(get_db)):
    """Lista todas las acciones visibles en este informe:
    - Acciones creadas en este informe
    - Acciones de informes anteriores que están PENDIENTE o EN_PROCESO
    """
    informe = _get_informe_or_404(informe_id, db)

    # IDs de informes anteriores del mismo contrato
    informe_ids_anteriores = (
        db.query(InformeSemanal.id)
        .filter(
            InformeSemanal.contrato_obra_id == informe.contrato_obra_id,
            InformeSemanal.id < informe.id,
        )
        .subquery()
    )

    # Acciones de este informe (todas) + acciones pendientes/en_proceso de anteriores
    acciones = (
        db.query(AccionPlan)
        .filter(
            (AccionPlan.informe_origen_id == informe_id)
            | (
                AccionPlan.informe_origen_id.in_(informe_ids_anteriores)
                & AccionPlan.estado.in_([
                    EstadoPlanAccion.PENDIENTE,
                    EstadoPlanAccion.EN_PROCESO,
                    EstadoPlanAccion.VENCIDO,
                ])
            )
        )
        .order_by(AccionPlan.numero)
        .all()
    )
    return acciones


@router.post(
    "",
    response_model=AccionPlanResponse,
    status_code=status.HTTP_201_CREATED,
)
def crear_accion_plan(
    informe_id: int, data: AccionPlanCreate, db: Session = Depends(get_db)
):
    informe = _get_informe_or_404(informe_id, db)
    if informe.estado != EstadoInforme.BORRADOR:
        raise HTTPException(
            status_code=400,
            detail="Solo se pueden crear acciones en informes en estado BORRADOR",
        )

    # Calcular siguiente numero
    max_num = (
        db.query(AccionPlan.numero)
        .filter(AccionPlan.informe_origen_id == informe_id)
        .order_by(AccionPlan.numero.desc())
        .first()
    )
    siguiente_numero = (max_num[0] + 1) if max_num else 1

    accion = AccionPlan(
        informe_origen_id=informe_id,
        numero=siguiente_numero,
        **data.model_dump(),
    )
    db.add(accion)
    db.commit()
    db.refresh(accion)
    return accion


@router.patch("/{accion_id}", response_model=AccionPlanResponse)
def actualizar_accion_plan(
    informe_id: int,
    accion_id: int,
    data: AccionPlanUpdate,
    db: Session = Depends(get_db),
):
    _get_informe_or_404(informe_id, db)

    accion = db.get(AccionPlan, accion_id)
    if not accion:
        raise HTTPException(status_code=404, detail="Acción no encontrada")

    update_data = data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(accion, field, value)
    db.commit()
    db.refresh(accion)
    return accion


@router.delete("/{accion_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_accion_plan(
    informe_id: int, accion_id: int, db: Session = Depends(get_db)
):
    informe = _get_informe_or_404(informe_id, db)
    if informe.estado != EstadoInforme.BORRADOR:
        raise HTTPException(
            status_code=400,
            detail="Solo se pueden eliminar acciones en informes en estado BORRADOR",
        )

    accion = db.get(AccionPlan, accion_id)
    if not accion:
        raise HTTPException(status_code=404, detail="Acción no encontrada")

    # Solo se pueden eliminar acciones creadas en este informe
    if accion.informe_origen_id != informe_id:
        raise HTTPException(
            status_code=400,
            detail="Solo se pueden eliminar acciones creadas en este informe",
        )

    db.delete(accion)
    db.commit()
