from datetime import date, datetime
from decimal import Decimal

from pydantic import BaseModel

from app.models.foto import TipoFoto


class FotoBase(BaseModel):
    pie_de_foto: str | None = None
    tipo: TipoFoto = TipoFoto.GENERAL
    fecha_toma: date
    latitud: Decimal | None = None
    longitud: Decimal | None = None


class FotoCreate(FotoBase):
    contrato_obra_id: int


class FotoResponse(FotoBase):
    id: int
    contrato_obra_id: int
    archivo_nombre: str
    archivo_path: str
    archivo_size_bytes: int
    subido_por_id: int | None
    created_at: datetime

    model_config = {"from_attributes": True}


class InformeFotoBase(BaseModel):
    foto_id: int
    orden: int = 0
    pie_de_foto_override: str | None = None


class InformeFotoCreate(InformeFotoBase):
    pass


class InformeFotoUpdate(BaseModel):
    orden: int | None = None
    pie_de_foto_override: str | None = None


class InformeFotoResponse(InformeFotoBase):
    id: int
    informe_semanal_id: int
    foto: FotoResponse

    model_config = {"from_attributes": True}
