from datetime import date
from decimal import Decimal

from pydantic import BaseModel

from app.models.informe import EstadoInforme


class InformeSemanalBase(BaseModel):
    numero_informe: int
    semana_inicio: date
    semana_fin: date


class InformeSemanalCreate(InformeSemanalBase):
    contrato_obra_id: int


class InformeSemanalUpdate(BaseModel):
    estado: EstadoInforme | None = None
    avance_fisico_programado: Decimal | None = None
    avance_fisico_ejecutado: Decimal | None = None
    valor_acumulado_programado: Decimal | None = None
    valor_acumulado_ejecutado: Decimal | None = None
    situaciones_problematicas: str | None = None
    actividades_no_previstas: str | None = None
    comentario_tecnico: str | None = None
    comentario_sst: str | None = None
    comentario_ambiental: str | None = None
    comentario_social: str | None = None


class InformeSemanalResponse(InformeSemanalBase):
    id: int
    contrato_obra_id: int
    estado: EstadoInforme
    avance_fisico_programado: Decimal
    avance_fisico_ejecutado: Decimal
    valor_acumulado_programado: Decimal
    valor_acumulado_ejecutado: Decimal
    situaciones_problematicas: str | None
    actividades_no_previstas: str | None
    comentario_tecnico: str | None
    comentario_sst: str | None
    comentario_ambiental: str | None
    comentario_social: str | None

    model_config = {"from_attributes": True}
