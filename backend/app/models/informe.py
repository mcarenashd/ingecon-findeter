import enum
from datetime import date, datetime, timezone
from decimal import Decimal

from sqlalchemy import Date, DateTime, Enum, ForeignKey, Integer, Numeric, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class EstadoInforme(str, enum.Enum):
    BORRADOR = "borrador"
    EN_REVISION = "en_revision"
    APROBADO = "aprobado"
    RADICADO = "radicado"


class InformeSemanal(Base):
    __tablename__ = "informes_semanales"

    id: Mapped[int] = mapped_column(primary_key=True)
    contrato_obra_id: Mapped[int] = mapped_column(ForeignKey("contratos_obra.id"))
    numero_informe: Mapped[int] = mapped_column(Integer)
    semana_inicio: Mapped[date] = mapped_column(Date)
    semana_fin: Mapped[date] = mapped_column(Date)
    estado: Mapped[EstadoInforme] = mapped_column(
        Enum(EstadoInforme), default=EstadoInforme.BORRADOR
    )

    # Sección 2 - Indicadores (calculados automáticamente)
    avance_fisico_programado: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=0)
    avance_fisico_ejecutado: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=0)
    valor_acumulado_programado: Mapped[Decimal] = mapped_column(Numeric(18, 2), default=0)
    valor_acumulado_ejecutado: Mapped[Decimal] = mapped_column(Numeric(18, 2), default=0)

    # Sección 3 - Situaciones Problemáticas
    situaciones_problematicas: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Sección 5 - Actividades No Previstas
    actividades_no_previstas: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Sección 6 - Comentarios del Interventor
    comentario_tecnico: Mapped[str | None] = mapped_column(Text, nullable=True)
    comentario_sst: Mapped[str | None] = mapped_column(Text, nullable=True)
    comentario_ambiental: Mapped[str | None] = mapped_column(Text, nullable=True)
    comentario_social: Mapped[str | None] = mapped_column(Text, nullable=True)

    contrato_obra: Mapped["ContratoObra"] = relationship(back_populates="informes_semanales")

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )
    creado_por_id: Mapped[int | None] = mapped_column(
        ForeignKey("usuarios.id"), nullable=True
    )


from app.models.contrato import ContratoObra  # noqa: E402
