from datetime import date, datetime

from pydantic import BaseModel

from app.models.informe import EstadoPlanAccion


class AccionPlanBase(BaseModel):
    actividad: str
    responsable: str
    responsable_usuario_id: int | None = None
    fecha_programada: date


class AccionPlanCreate(AccionPlanBase):
    pass


class AccionPlanUpdate(BaseModel):
    actividad: str | None = None
    responsable: str | None = None
    responsable_usuario_id: int | None = None
    fecha_programada: date | None = None
    fecha_cumplimiento: date | None = None
    estado: EstadoPlanAccion | None = None
    observaciones: str | None = None


class AccionPlanResponse(AccionPlanBase):
    id: int
    numero: int
    informe_origen_id: int
    fecha_cumplimiento: date | None
    estado: EstadoPlanAccion
    observaciones: str | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}
