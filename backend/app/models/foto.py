import enum
from datetime import date, datetime, timezone
from decimal import Decimal

from sqlalchemy import Date, DateTime, Enum, ForeignKey, Integer, Numeric, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base


class TipoFoto(str, enum.Enum):
    AVANCE = "avance"
    SST = "sst"
    AMBIENTAL = "ambiental"
    SOCIAL = "social"
    GENERAL = "general"


class Foto(Base):
    __tablename__ = "fotos"

    id: Mapped[int] = mapped_column(primary_key=True)
    contrato_obra_id: Mapped[int] = mapped_column(ForeignKey("contratos_obra.id"))

    # Archivo
    archivo_nombre: Mapped[str] = mapped_column(String(500))
    archivo_path: Mapped[str] = mapped_column(String(1000))
    archivo_size_bytes: Mapped[int] = mapped_column(Integer)

    # Metadata
    pie_de_foto: Mapped[str | None] = mapped_column(Text, nullable=True)
    tipo: Mapped[TipoFoto] = mapped_column(
        Enum(TipoFoto, values_callable=lambda e: [m.value for m in e]),
        default=TipoFoto.GENERAL,
    )
    fecha_toma: Mapped[date] = mapped_column(Date)
    latitud: Mapped[Decimal | None] = mapped_column(Numeric(10, 7), nullable=True)
    longitud: Mapped[Decimal | None] = mapped_column(Numeric(10, 7), nullable=True)

    # Auditoría
    subido_por_id: Mapped[int | None] = mapped_column(
        ForeignKey("usuarios.id"), nullable=True
    )
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    contrato_obra: Mapped["ContratoObra"] = relationship(back_populates="fotos")
    informes: Mapped[list["InformeFoto"]] = relationship(back_populates="foto")


# Forward references
from app.models.contrato import ContratoObra  # noqa: E402
from app.models.informe import InformeFoto  # noqa: E402
