"""
Seed script — popula la base de datos con datos iniciales del contrato
FDT-ATBOSA-I-028-2025 (Consorcio Infraestructura Bosa / Findeter).

Uso:
    cd backend
    python -m app.scripts.seed
"""

from datetime import date
from decimal import Decimal

from sqlalchemy.orm import Session

from app.core.database import SessionLocal, engine
from app.core.database import Base  # noqa: F401  — importar para que metadata tenga las tablas
from app.core.security import get_password_hash
from app.models.contrato import (
    ActividadNoPrevista,
    ContratoInterventoria,
    ContratoObra,
    EstadoHito,
    Hito,
)
from app.models.usuario import RolUsuario, Usuario

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
DEFAULT_PASSWORD = get_password_hash("Ingecon2026!")


def _already_seeded(db: Session) -> bool:
    return db.query(ContratoInterventoria).first() is not None


# ---------------------------------------------------------------------------
# 1. Usuarios (7 roles)
# ---------------------------------------------------------------------------
USUARIOS = [
    {
        "email": "director@ingecon.co",
        "nombre_completo": "Carlos Martínez López",
        "rol": RolUsuario.DIRECTOR,
    },
    {
        "email": "tecnico@ingecon.co",
        "nombre_completo": "Ana María Rodríguez",
        "rol": RolUsuario.RESIDENTE_TECNICO,
    },
    {
        "email": "sst@ingecon.co",
        "nombre_completo": "Jorge Hernández Díaz",
        "rol": RolUsuario.RESIDENTE_SST,
    },
    {
        "email": "ambiental@ingecon.co",
        "nombre_completo": "Laura Gómez Vargas",
        "rol": RolUsuario.RESIDENTE_AMBIENTAL,
    },
    {
        "email": "social@ingecon.co",
        "nombre_completo": "María Fernanda Torres",
        "rol": RolUsuario.RESIDENTE_SOCIAL,
    },
    {
        "email": "admin@ingecon.co",
        "nombre_completo": "Pedro Sánchez Ruiz",
        "rol": RolUsuario.RESIDENTE_ADMINISTRATIVO,
    },
    {
        "email": "supervisor@findeter.gov.co",
        "nombre_completo": "Roberto Castillo Mejía",
        "rol": RolUsuario.SUPERVISOR,
    },
]


# ---------------------------------------------------------------------------
# 2. Contrato de Interventoría
# ---------------------------------------------------------------------------
CONTRATO_INTERVENTORIA = {
    "numero": "FDT-ATBOSA-I-028-2025",
    "objeto": (
        "Interventoría técnica, administrativa, financiera, contable, jurídica, "
        "ambiental, SST y social para la construcción y dotación de parques vecinales "
        "y/o de bolsillo en la localidad de Bosa, Bogotá D.C."
    ),
    "valor_inicial": Decimal("1650000000.00"),
    "valor_actualizado": Decimal("1650000000.00"),
    "plazo_dias": 540,
    "fecha_inicio": date(2025, 7, 15),
    "fecha_terminacion": date(2027, 1, 5),
    "contratista": "Consorcio Infraestructura Bosa",
    "supervisor": "Findeter S.A.",
}


# ---------------------------------------------------------------------------
# 3. Contratos de Obra (4 parques)
# ---------------------------------------------------------------------------
CONTRATOS_OBRA = [
    {
        "numero": "CTO-703-2025",
        "objeto": "Construcción y dotación Parque Vecinal La Esperanza, Bosa",
        "contratista": "Consorcio Parques Bosa I",
        "valor_inicial": Decimal("3200000000.00"),
        "adiciones": Decimal("0.00"),
        "valor_actualizado": Decimal("3200000000.00"),
        "plazo_dias": 360,
        "fecha_inicio": date(2025, 8, 1),
        "fecha_terminacion": date(2026, 7, 27),
    },
    {
        "numero": "CTO-704-2025",
        "objeto": "Construcción y dotación Parque Vecinal Piamonte, Bosa",
        "contratista": "Consorcio Parques Bosa I",
        "valor_inicial": Decimal("2800000000.00"),
        "adiciones": Decimal("0.00"),
        "valor_actualizado": Decimal("2800000000.00"),
        "plazo_dias": 360,
        "fecha_inicio": date(2025, 8, 1),
        "fecha_terminacion": date(2026, 7, 27),
    },
    {
        "numero": "CTO-705-2025",
        "objeto": "Construcción y dotación Parque de Bolsillo San Bernardino, Bosa",
        "contratista": "Consorcio Parques Bosa II",
        "valor_inicial": Decimal("1500000000.00"),
        "adiciones": Decimal("0.00"),
        "valor_actualizado": Decimal("1500000000.00"),
        "plazo_dias": 270,
        "fecha_inicio": date(2025, 9, 1),
        "fecha_terminacion": date(2026, 5, 29),
    },
    {
        "numero": "CTO-706-2025",
        "objeto": "Construcción y dotación Parque de Bolsillo El Recreo, Bosa",
        "contratista": "Consorcio Parques Bosa II",
        "valor_inicial": Decimal("1200000000.00"),
        "adiciones": Decimal("0.00"),
        "valor_actualizado": Decimal("1200000000.00"),
        "plazo_dias": 270,
        "fecha_inicio": date(2025, 9, 1),
        "fecha_terminacion": date(2026, 5, 29),
    },
]


# ---------------------------------------------------------------------------
# 4. Hitos por contrato de obra
#    20 hitos para La Esperanza (CTO-703) y Piamonte (CTO-704)
#    12 hitos para los parques de bolsillo (CTO-705, CTO-706)
# ---------------------------------------------------------------------------
def _hitos_parque_vecinal(contrato_obra_id: int, fecha_inicio: date) -> list[dict]:
    """20 hitos típicos de un parque vecinal grande."""
    from datetime import timedelta

    hitos = [
        (1, "Instalación de campamento y señalización de obra", 7),
        (2, "Cerramiento perimetral y control de acceso", 14),
        (3, "Demoliciones y retiro de escombros", 30),
        (4, "Excavación y movimiento de tierras", 45),
        (5, "Cimentación — zapatas y vigas de amarre", 60),
        (6, "Estructura en concreto — placa base", 75),
        (7, "Redes hidrosanitarias subterráneas", 90),
        (8, "Redes eléctricas subterráneas y alumbrado", 105),
        (9, "Construcción de senderos peatonales", 120),
        (10, "Instalación de bordillos y sardineles", 135),
        (11, "Construcción de canchas deportivas", 150),
        (12, "Construcción de zona de juegos infantiles", 165),
        (13, "Instalación de mobiliario urbano (bancas, canecas)", 180),
        (14, "Sistema de riego automatizado", 210),
        (15, "Empradización y arborización", 240),
        (16, "Instalación de luminarias y postes", 260),
        (17, "Pintura, señalización y acabados", 290),
        (18, "Pruebas de redes y certificaciones", 320),
        (19, "Entrega parcial y socialización con la comunidad", 340),
        (20, "Entrega final y acta de recibo a satisfacción", 360),
    ]
    return [
        {
            "contrato_obra_id": contrato_obra_id,
            "numero": num,
            "descripcion": desc,
            "fecha_programada": fecha_inicio + timedelta(days=days),
            "fecha_real": None,
            "estado": EstadoHito.NO_INICIADO,
            "avance_porcentaje": Decimal("0.00"),
        }
        for num, desc, days in hitos
    ]


def _hitos_parque_bolsillo(contrato_obra_id: int, fecha_inicio: date) -> list[dict]:
    """12 hitos para un parque de bolsillo (más pequeño)."""
    from datetime import timedelta

    hitos = [
        (1, "Instalación de campamento y señalización", 7),
        (2, "Cerramiento y control de acceso", 14),
        (3, "Demoliciones menores y retiro de material", 25),
        (4, "Excavación y nivelación del terreno", 40),
        (5, "Cimentación y placa base", 60),
        (6, "Redes hidrosanitarias y eléctricas", 90),
        (7, "Construcción de senderos y zonas duras", 120),
        (8, "Zona de juegos y mobiliario", 150),
        (9, "Empradización y jardinería", 190),
        (10, "Alumbrado público y luminarias", 220),
        (11, "Acabados, pintura y señalización", 250),
        (12, "Entrega final y acta de recibo", 270),
    ]
    return [
        {
            "contrato_obra_id": contrato_obra_id,
            "numero": num,
            "descripcion": desc,
            "fecha_programada": fecha_inicio + timedelta(days=days),
            "fecha_real": None,
            "estado": EstadoHito.NO_INICIADO,
            "avance_porcentaje": Decimal("0.00"),
        }
        for num, desc, days in hitos
    ]


# ---------------------------------------------------------------------------
# 5. Actividades No Previstas (vinculadas a CTO-703 y CTO-704)
# ---------------------------------------------------------------------------
ACTIVIDADES_NP_703 = [
    ("NP-01", "Retiro de redes de servicios públicos no identificadas en diseño"),
    ("NP-02", "Estabilización de talud costado norte por hallazgo de suelo inestable"),
    ("NP-03", "Reubicación de poste de alumbrado público existente"),
    ("NP-04", "Construcción de muro de contención adicional"),
    ("NP-05", "Manejo de aguas freáticas no previstas en excavación"),
    ("NP-06", "Retiro de escombros y residuos enterrados"),
    ("NP-07", "Adecuación de acceso vehicular temporal por cierre vial"),
    ("NP-08", "Protección de árboles existentes no contemplados en inventario forestal"),
    ("NP-09", "Refuerzo de cimentación por hallazgo de relleno no controlado"),
    ("NP-10", "Instalación de señalización temporal adicional por requerimiento del IDIGER"),
    ("NP-11", "Adecuación de drenaje pluvial por cambio de nivel freático"),
]

ACTIVIDADES_NP_704 = [
    ("NP-12", "Demolición de estructura enterrada no identificada en estudios previos"),
    ("NP-13", "Reubicación de red de gas natural por interferencia con diseño"),
    ("NP-14", "Estabilización de terreno por presencia de arcilla expansiva"),
    ("NP-15", "Construcción de cuneta perimetral no prevista"),
    ("NP-16", "Manejo de hallazgo arqueológico — protocolo ICANH"),
    ("NP-17", "Protección temporal de fauna silvestre encontrada en el predio"),
    ("NP-18", "Adecuación de campamento por requisito ambiental adicional de la CAR"),
    ("NP-19", "Refuerzo de vía de acceso deteriorada por tráfico pesado de obra"),
    ("NP-20", "Instalación de barreras antirruido por queja de comunidad vecina"),
    ("NP-21", "Manejo de interferencia con red de acueducto no registrada en planos"),
    ("NP-22", "Replanteo de sendero por hallazgo de raíces de árbol protegido"),
]


# ---------------------------------------------------------------------------
# Seed runner
# ---------------------------------------------------------------------------
def seed(db: Session) -> None:
    if _already_seeded(db):
        print("La base de datos ya tiene datos. Omitiendo seed.")
        return

    # --- Usuarios ---
    usuarios = []
    for u in USUARIOS:
        usuario = Usuario(
            email=u["email"],
            nombre_completo=u["nombre_completo"],
            hashed_password=DEFAULT_PASSWORD,
            rol=u["rol"],
            activo=True,
        )
        db.add(usuario)
        usuarios.append(usuario)
    db.flush()
    print(f"  + {len(usuarios)} usuarios creados")

    # --- Contrato de Interventoría ---
    ci = ContratoInterventoria(**CONTRATO_INTERVENTORIA)
    db.add(ci)
    db.flush()
    print(f"  + Contrato interventoría: {ci.numero}")

    # --- Contratos de Obra ---
    contratos_obra = []
    for co_data in CONTRATOS_OBRA:
        co = ContratoObra(contrato_interventoria_id=ci.id, **co_data)
        db.add(co)
        contratos_obra.append(co)
    db.flush()
    print(f"  + {len(contratos_obra)} contratos de obra creados")

    # --- Hitos ---
    total_hitos = 0
    for co in contratos_obra:
        if co.numero in ("CTO-703-2025", "CTO-704-2025"):
            hitos_data = _hitos_parque_vecinal(co.id, co.fecha_inicio)
        else:
            hitos_data = _hitos_parque_bolsillo(co.id, co.fecha_inicio)

        for h_data in hitos_data:
            db.add(Hito(**h_data))
            total_hitos += 1
    db.flush()
    print(f"  + {total_hitos} hitos creados")

    # --- Actividades No Previstas ---
    co_703 = contratos_obra[0]  # CTO-703
    co_704 = contratos_obra[1]  # CTO-704

    total_anp = 0
    for codigo, descripcion in ACTIVIDADES_NP_703:
        db.add(
            ActividadNoPrevista(
                contrato_obra_id=co_703.id,
                codigo=codigo,
                descripcion=descripcion,
            )
        )
        total_anp += 1

    for codigo, descripcion in ACTIVIDADES_NP_704:
        db.add(
            ActividadNoPrevista(
                contrato_obra_id=co_704.id,
                codigo=codigo,
                descripcion=descripcion,
            )
        )
        total_anp += 1

    db.flush()
    print(f"  + {total_anp} actividades no previstas creadas")

    db.commit()
    print("\nSeed completado exitosamente.")


def main() -> None:
    print("Ejecutando seed de datos iniciales...")
    print("=" * 50)
    db = SessionLocal()
    try:
        seed(db)
    except Exception as e:
        db.rollback()
        print(f"\nError durante seed: {e}")
        raise
    finally:
        db.close()


if __name__ == "__main__":
    # Asegurar que todos los modelos estén registrados
    import app.models  # noqa: F401

    main()
