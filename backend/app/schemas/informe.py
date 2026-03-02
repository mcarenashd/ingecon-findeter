from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel

from app.models.contrato import EstadoHito
from app.models.informe import EstadoInforme


# --- Request schemas ---


class InformeGenerarRequest(BaseModel):
    contrato_obra_id: int
    semana_inicio: date
    semana_fin: date


class InformeSemanalCreate(BaseModel):
    contrato_obra_id: int
    numero_informe: int
    semana_inicio: date
    semana_fin: date


class InformeSemanalUpdate(BaseModel):
    estado: EstadoInforme | None = None
    avance_fisico_programado: Decimal | None = None
    avance_fisico_ejecutado: Decimal | None = None
    valor_acumulado_programado: Decimal | None = None
    valor_acumulado_ejecutado: Decimal | None = None
    situaciones_problematicas: str | None = None
    actividades_no_previstas: str | None = None
    actividades_no_previstas_narrativa: str | None = None
    comentario_tecnico: str | None = None
    comentario_sst: str | None = None
    comentario_ambiental: str | None = None
    comentario_social: str | None = None


# Schemas por sección (para edición por rol)

class InformeSemanalUpdateS3(BaseModel):
    situaciones_problematicas: str | None = None


class InformeSemanalUpdateS5(BaseModel):
    actividades_no_previstas: str | None = None
    actividades_no_previstas_narrativa: str | None = None


class InformeSemanalUpdateS6Tecnico(BaseModel):
    comentario_tecnico: str | None = None


class InformeSemanalUpdateS6SST(BaseModel):
    comentario_sst: str | None = None


class InformeSemanalUpdateS6Ambiental(BaseModel):
    comentario_ambiental: str | None = None


class InformeSemanalUpdateS6Social(BaseModel):
    comentario_social: str | None = None


class InformeTransicionEstado(BaseModel):
    nuevo_estado: EstadoInforme


# --- Response schemas ---


class SnapshotHitoResponse(BaseModel):
    id: int
    hito_id: int
    numero: int
    descripcion: str
    fecha_programada: date
    fecha_real: date | None
    estado: EstadoHito
    avance_porcentaje: Decimal
    dias_retraso: int

    model_config = {"from_attributes": True}


class InformeSemanalListResponse(BaseModel):
    id: int
    contrato_obra_id: int
    numero_informe: int
    semana_inicio: date
    semana_fin: date
    estado: EstadoInforme
    avance_fisico_ejecutado: Decimal
    updated_at: datetime

    model_config = {"from_attributes": True}


class InformeSemanalResponse(BaseModel):
    id: int
    contrato_obra_id: int
    numero_informe: int
    semana_inicio: date
    semana_fin: date
    estado: EstadoInforme
    avance_fisico_programado: Decimal
    avance_fisico_ejecutado: Decimal
    valor_acumulado_programado: Decimal
    valor_acumulado_ejecutado: Decimal
    situaciones_problematicas: str | None
    actividades_no_previstas: str | None
    actividades_no_previstas_narrativa: str | None
    comentario_tecnico: str | None
    comentario_sst: str | None
    comentario_ambiental: str | None
    comentario_social: str | None
    fecha_envio_revision: datetime | None
    fecha_aprobacion: datetime | None
    fecha_radicacion: datetime | None
    aprobado_por_id: int | None
    creado_por_id: int | None
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class InformeSemanalDetailResponse(InformeSemanalResponse):
    snapshot_hitos: list[SnapshotHitoResponse] = []


# --- Curva S ---


class CurvaSDataPoint(BaseModel):
    semana: int
    semana_fin: date
    programado: Decimal
    ejecutado: Decimal


class CurvaSResponse(BaseModel):
    contrato_obra_id: int
    contrato_numero: str
    datos: list[CurvaSDataPoint]
