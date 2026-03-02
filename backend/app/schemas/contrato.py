from datetime import date
from decimal import Decimal

from pydantic import BaseModel

from app.models.contrato import EstadoHito


class ContratoInterventoriaBase(BaseModel):
    numero: str
    objeto: str
    valor_inicial: Decimal
    valor_actualizado: Decimal
    plazo_dias: int
    fecha_inicio: date
    fecha_terminacion: date
    contratista: str
    supervisor: str


class ContratoInterventoriaCreate(ContratoInterventoriaBase):
    pass


class ContratoInterventoriaResponse(ContratoInterventoriaBase):
    id: int

    model_config = {"from_attributes": True}


class ContratoObraBase(BaseModel):
    numero: str
    objeto: str
    contratista: str
    valor_inicial: Decimal
    adiciones: Decimal = Decimal("0")
    valor_actualizado: Decimal
    plazo_dias: int
    fecha_inicio: date
    fecha_terminacion: date
    fecha_suspension: date | None = None
    fecha_reinicio: date | None = None


class ContratoObraCreate(ContratoObraBase):
    contrato_interventoria_id: int


class ContratoObraResponse(ContratoObraBase):
    id: int
    contrato_interventoria_id: int

    model_config = {"from_attributes": True}


class HitoBase(BaseModel):
    numero: int
    descripcion: str
    fecha_programada: date
    fecha_real: date | None = None
    estado: EstadoHito = EstadoHito.NO_INICIADO
    avance_porcentaje: Decimal = Decimal("0")


class HitoCreate(HitoBase):
    contrato_obra_id: int


class HitoResponse(HitoBase):
    id: int
    contrato_obra_id: int
    dias_retraso: int

    model_config = {"from_attributes": True}
