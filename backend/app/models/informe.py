import enum
from datetime import date, datetime, timezone
from decimal import Decimal

from sqlalchemy import Date, DateTime, Enum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base
from app.models.contrato import EstadoHito


class EstadoInforme(str, enum.Enum):
    BORRADOR = "borrador"
    EN_REVISION = "en_revision"
    APROBADO = "aprobado"
    RADICADO = "radicado"


class EstadoPlanAccion(str, enum.Enum):
    PENDIENTE = "pendiente"
    EN_PROCESO = "en_proceso"
    CUMPLIDO = "cumplido"
    VENCIDO = "vencido"


class InformeSemanal(Base):
    __tablename__ = "informes_semanales"

    id: Mapped[int] = mapped_column(primary_key=True)
    contrato_obra_id: Mapped[int] = mapped_column(ForeignKey("contratos_obra.id"))
    numero_informe: Mapped[int] = mapped_column(Integer)
    semana_inicio: Mapped[date] = mapped_column(Date)
    semana_fin: Mapped[date] = mapped_column(Date)
    estado: Mapped[EstadoInforme] = mapped_column(
        Enum(EstadoInforme, values_callable=lambda e: [m.value for m in e]),
        default=EstadoInforme.BORRADOR,
    )

    # Sección 2 - Indicadores (calculados automáticamente)
    avance_fisico_programado: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=0)
    avance_fisico_ejecutado: Mapped[Decimal] = mapped_column(Numeric(5, 2), default=0)
    valor_acumulado_programado: Mapped[Decimal] = mapped_column(Numeric(18, 2), default=0)
    valor_acumulado_ejecutado: Mapped[Decimal] = mapped_column(Numeric(18, 2), default=0)

    # Sección 3 - Situaciones Problemáticas
    situaciones_problematicas: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Sección 5 - Actividades No Previstas (narrativa, la tabla viene de ActividadNoPrevista)
    actividades_no_previstas: Mapped[str | None] = mapped_column(Text, nullable=True)
    actividades_no_previstas_narrativa: Mapped[str | None] = mapped_column(
        Text, nullable=True
    )

    # Sección 6 - Comentarios del Interventor
    comentario_tecnico: Mapped[str | None] = mapped_column(Text, nullable=True)
    comentario_sst: Mapped[str | None] = mapped_column(Text, nullable=True)
    comentario_ambiental: Mapped[str | None] = mapped_column(Text, nullable=True)
    comentario_social: Mapped[str | None] = mapped_column(Text, nullable=True)

    # Trazabilidad de transiciones de estado
    fecha_envio_revision: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    fecha_aprobacion: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    fecha_radicacion: Mapped[datetime | None] = mapped_column(
        DateTime(timezone=True), nullable=True
    )
    aprobado_por_id: Mapped[int | None] = mapped_column(
        ForeignKey("usuarios.id"), nullable=True
    )

    # Auditoría
    creado_por_id: Mapped[int | None] = mapped_column(
        ForeignKey("usuarios.id"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    # Relaciones
    contrato_obra: Mapped["ContratoObra"] = relationship(back_populates="informes_semanales")
    snapshot_hitos: Mapped[list["SnapshotHito"]] = relationship(
        back_populates="informe_semanal", cascade="all, delete-orphan"
    )
    fotos_seleccionadas: Mapped[list["InformeFoto"]] = relationship(
        back_populates="informe_semanal", cascade="all, delete-orphan"
    )
    acciones_plan: Mapped[list["AccionPlan"]] = relationship(
        back_populates="informe_origen",
        foreign_keys="AccionPlan.informe_origen_id",
    )


class SnapshotHito(Base):
    __tablename__ = "snapshot_hitos"

    id: Mapped[int] = mapped_column(primary_key=True)
    informe_semanal_id: Mapped[int] = mapped_column(ForeignKey("informes_semanales.id"))
    hito_id: Mapped[int] = mapped_column(ForeignKey("hitos.id"))

    # Copia inmutable del estado del hito al momento del corte
    numero: Mapped[int] = mapped_column(Integer)
    descripcion: Mapped[str] = mapped_column(Text)
    fecha_programada: Mapped[date] = mapped_column(Date)
    fecha_real: Mapped[date | None] = mapped_column(Date, nullable=True)
    estado: Mapped[EstadoHito] = mapped_column(Enum(EstadoHito, values_callable=lambda e: [m.value for m in e]))
    avance_porcentaje: Mapped[Decimal] = mapped_column(Numeric(5, 2))
    dias_retraso: Mapped[int] = mapped_column(Integer, default=0)

    informe_semanal: Mapped["InformeSemanal"] = relationship(back_populates="snapshot_hitos")


class InformeFoto(Base):
    __tablename__ = "informe_fotos"

    id: Mapped[int] = mapped_column(primary_key=True)
    informe_semanal_id: Mapped[int] = mapped_column(ForeignKey("informes_semanales.id"))
    foto_id: Mapped[int] = mapped_column(ForeignKey("fotos.id"))
    orden: Mapped[int] = mapped_column(Integer, default=0)
    pie_de_foto_override: Mapped[str | None] = mapped_column(Text, nullable=True)

    informe_semanal: Mapped["InformeSemanal"] = relationship(
        back_populates="fotos_seleccionadas"
    )
    foto: Mapped["Foto"] = relationship(back_populates="informes")


class AccionPlan(Base):
    __tablename__ = "acciones_plan"

    id: Mapped[int] = mapped_column(primary_key=True)
    informe_origen_id: Mapped[int] = mapped_column(ForeignKey("informes_semanales.id"))

    numero: Mapped[int] = mapped_column(Integer)
    actividad: Mapped[str] = mapped_column(Text)
    responsable: Mapped[str] = mapped_column(String(255))
    responsable_usuario_id: Mapped[int | None] = mapped_column(
        ForeignKey("usuarios.id"), nullable=True
    )
    fecha_programada: Mapped[date] = mapped_column(Date)
    fecha_cumplimiento: Mapped[date | None] = mapped_column(Date, nullable=True)
    estado: Mapped[EstadoPlanAccion] = mapped_column(
        Enum(EstadoPlanAccion, values_callable=lambda e: [m.value for m in e]),
        default=EstadoPlanAccion.PENDIENTE,
    )
    observaciones: Mapped[str | None] = mapped_column(Text, nullable=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    informe_origen: Mapped["InformeSemanal"] = relationship(
        back_populates="acciones_plan",
        foreign_keys=[informe_origen_id],
    )


# Forward references
from app.models.contrato import ContratoObra  # noqa: E402
from app.models.foto import Foto  # noqa: E402
