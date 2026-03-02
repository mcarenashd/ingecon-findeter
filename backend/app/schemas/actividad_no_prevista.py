from datetime import date

from pydantic import BaseModel


class ActividadNoPrevistaBase(BaseModel):
    codigo: str
    descripcion: str
    fecha_programada: date | None = None
    fecha_real: date | None = None


class ActividadNoPrevistaCreate(ActividadNoPrevistaBase):
    pass


class ActividadNoPrevistaUpdate(BaseModel):
    codigo: str | None = None
    descripcion: str | None = None
    fecha_programada: date | None = None
    fecha_real: date | None = None


class ActividadNoPrevistaResponse(ActividadNoPrevistaBase):
    id: int
    contrato_obra_id: int

    model_config = {"from_attributes": True}
