import enum
from datetime import date, datetime, timezone
from decimal import Decimal

from sqlalchemy import (
    Date,
    DateTime,
    Enum,
    ForeignKey,
    Integer,
    Numeric,
    String,
    Text,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class EstadoHito(str, enum.Enum):
    NO_INICIADO = "no_iniciado"
    EN_PROCESO = "en_proceso"
    CUMPLIDO = "cumplido"
    VENCIDO = "vencido"


class ContratoInterventoria(Base):
    __tablename__ = "contratos_interventoria"

    id: Mapped[int] = mapped_column(primary_key=True)
    numero: Mapped[str] = mapped_column(String(100), unique=True)
    objeto: Mapped[str] = mapped_column(Text)
    valor_inicial: Mapped[Decimal] = mapped_column(Numeric(18, 2))
    valor_actualizado: Mapped[Decimal] = mapped_column(Numeric(18, 2))
    plazo_dias: Mapped[int] = mapped_column(Integer)
    fecha_inicio: Mapped[date] = mapped_column(Date)
    fecha_terminacion: Mapped[date] = mapped_column(Date)
    contratista: Mapped[str] = mapped_column(String(255))
    supervisor: Mapped[str] = mapped_column(String(255))

    contratos_obra: Mapped[list["ContratoObra"]] = relationship(back_populates="contrato_interventoria")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )


class ContratoObra(Base):
    __tablename__ = "contratos_obra"

    id: Mapped[int] = mapped_column(primary_key=True)
    contrato_interventoria_id: Mapped[int] = mapped_column(
        ForeignKey("contratos_interventoria.id")
    )
    numero: Mapped[str] = mapped_column(String(100), unique=True)
    objeto: Mapped[str] = mapped_column(Text)
    contratista: Mapped[str] = mapped_column(String(255))
    valor_inicial: Mapped[Decimal] = mapped_column(Numeric(18, 2))
    adiciones: Mapped[Decimal] = mapped_column(Numeric(18, 2), default=0)
    valor_actualizado: Mapped[Decimal] = mapped_column(Numeric(18, 2))
    plazo_dias: Mapped[int] = mapped_column(Integer)
    fecha_inicio: Mapped[date] = mapped_column(Date)
    fecha_terminacion: Mapped[date] = mapped_column(Date)
    fecha_suspension: Mapped[date | None] = mapped_column(Date, nullable=True)
    fecha_reinicio: Mapped[date | None] = mapped_column(Date, nullable=True)

    contrato_interventoria: Mapped["ContratoInterventoria"] = relationship(
        back_populates="contratos_obra"
    )
    hitos: Mapped[list["Hito"]] = relationship(back_populates="contrato_obra")
    informes_semanales: Mapped[list["InformeSemanal"]] = relationship(
        back_populates="contrato_obra"
    )
    actividades_no_previstas: Mapped[list["ActividadNoPrevista"]] = relationship(
        back_populates="contrato_obra"
    )
    fotos: Mapped[list["Foto"]] = relationship(back_populates="contrato_obra")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )


class Hito(Base):
    __tablename__ = "hitos"

    id: Mapped[int] = mapped_column(primary_key=True)
    contrato_obra_id: Mapped[int] = mapped_column(ForeignKey("contratos_obra.id"))
    numero: Mapped[int] = mapped_column(Integer)
    descripcion: Mapped[str] = mapped_column(Text)
    fecha_programada: Mapped[date] = mapped_column(Date)
    fecha_real: Mapped[date | None] = mapped_column(Date, nullable=True)
    estado: Mapped[EstadoHito] = mapped_column(
        Enum(EstadoHito, values_callable=lambda e: [m.value for m in e]),
        default=EstadoHito.NO_INICIADO,
    )
    avance_porcentaje: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=0)

    contrato_obra: Mapped["ContratoObra"] = relationship(back_populates="hitos")

    @property
    def dias_retraso(self) -> int:
        if self.fecha_real and self.fecha_programada:
            delta = self.fecha_real - self.fecha_programada
            return max(0, delta.days)
        if not self.fecha_real and self.estado != EstadoHito.CUMPLIDO:
            from datetime import date as date_type
            delta = date_type.today() - self.fecha_programada
            return max(0, delta.days)
        return 0


class ActividadNoPrevista(Base):
    __tablename__ = "actividades_no_previstas"

    id: Mapped[int] = mapped_column(primary_key=True)
    contrato_obra_id: Mapped[int] = mapped_column(ForeignKey("contratos_obra.id"))
    codigo: Mapped[str] = mapped_column(String(20))  # e.g. "NP-01"
    descripcion: Mapped[str] = mapped_column(Text)
    fecha_programada: Mapped[date | None] = mapped_column(Date, nullable=True)
    fecha_real: Mapped[date | None] = mapped_column(Date, nullable=True)

    contrato_obra: Mapped["ContratoObra"] = relationship(
        back_populates="actividades_no_previstas"
    )


# Forward references
from app.models.foto import Foto  # noqa: E402
from app.models.informe import InformeSemanal  # noqa: E402
