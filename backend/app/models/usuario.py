import enum
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, String
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class RolUsuario(str, enum.Enum):
    DIRECTOR = "director_interventoria"
    RESIDENTE_TECNICO = "residente_tecnico"
    RESIDENTE_SST = "residente_sst"
    RESIDENTE_AMBIENTAL = "residente_ambiental"
    RESIDENTE_SOCIAL = "residente_social"
    RESIDENTE_ADMINISTRATIVO = "residente_administrativo"
    SUPERVISOR = "supervisor"


class Usuario(Base):
    __tablename__ = "usuarios"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(255), unique=True, index=True)
    nombre_completo: Mapped[str] = mapped_column(String(255))
    hashed_password: Mapped[str] = mapped_column(String(255))
    rol: Mapped[RolUsuario] = mapped_column(Enum(RolUsuario))
    activo: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
