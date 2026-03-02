"""initial — all models

Revision ID: 001
Revises: None
Create Date: 2026-03-02
"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

revision: str = "001"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # --- usuarios ---
    op.create_table(
        "usuarios",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("email", sa.String(255), unique=True, index=True, nullable=False),
        sa.Column("nombre_completo", sa.String(255), nullable=False),
        sa.Column("hashed_password", sa.String(255), nullable=False),
        sa.Column(
            "rol",
            sa.Enum(
                "director_interventoria",
                "residente_tecnico",
                "residente_sst",
                "residente_ambiental",
                "residente_social",
                "residente_administrativo",
                "supervisor",
                name="rolusuario",
            ),
            nullable=False,
        ),
        sa.Column("activo", sa.Boolean(), server_default=sa.text("true"), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )

    # --- contratos_interventoria ---
    op.create_table(
        "contratos_interventoria",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column("numero", sa.String(100), unique=True, nullable=False),
        sa.Column("objeto", sa.Text(), nullable=False),
        sa.Column("valor_inicial", sa.Numeric(18, 2), nullable=False),
        sa.Column("valor_actualizado", sa.Numeric(18, 2), nullable=False),
        sa.Column("plazo_dias", sa.Integer(), nullable=False),
        sa.Column("fecha_inicio", sa.Date(), nullable=False),
        sa.Column("fecha_terminacion", sa.Date(), nullable=False),
        sa.Column("contratista", sa.String(255), nullable=False),
        sa.Column("supervisor", sa.String(255), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )

    # --- contratos_obra ---
    op.create_table(
        "contratos_obra",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "contrato_interventoria_id",
            sa.Integer(),
            sa.ForeignKey("contratos_interventoria.id"),
            nullable=False,
        ),
        sa.Column("numero", sa.String(100), unique=True, nullable=False),
        sa.Column("objeto", sa.Text(), nullable=False),
        sa.Column("contratista", sa.String(255), nullable=False),
        sa.Column("valor_inicial", sa.Numeric(18, 2), nullable=False),
        sa.Column("adiciones", sa.Numeric(18, 2), server_default=sa.text("0"), nullable=False),
        sa.Column("valor_actualizado", sa.Numeric(18, 2), nullable=False),
        sa.Column("plazo_dias", sa.Integer(), nullable=False),
        sa.Column("fecha_inicio", sa.Date(), nullable=False),
        sa.Column("fecha_terminacion", sa.Date(), nullable=False),
        sa.Column("fecha_suspension", sa.Date(), nullable=True),
        sa.Column("fecha_reinicio", sa.Date(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )

    # --- hitos ---
    op.create_table(
        "hitos",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "contrato_obra_id",
            sa.Integer(),
            sa.ForeignKey("contratos_obra.id"),
            nullable=False,
        ),
        sa.Column("numero", sa.Integer(), nullable=False),
        sa.Column("descripcion", sa.Text(), nullable=False),
        sa.Column("fecha_programada", sa.Date(), nullable=False),
        sa.Column("fecha_real", sa.Date(), nullable=True),
        sa.Column(
            "estado",
            sa.Enum("no_iniciado", "en_proceso", "cumplido", "vencido", name="estadohito"),
            server_default=sa.text("'no_iniciado'"),
            nullable=False,
        ),
        sa.Column("avance_porcentaje", sa.Numeric(5, 2), server_default=sa.text("0"), nullable=False),
    )

    # --- actividades_no_previstas ---
    op.create_table(
        "actividades_no_previstas",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "contrato_obra_id",
            sa.Integer(),
            sa.ForeignKey("contratos_obra.id"),
            nullable=False,
        ),
        sa.Column("codigo", sa.String(20), nullable=False),
        sa.Column("descripcion", sa.Text(), nullable=False),
        sa.Column("fecha_programada", sa.Date(), nullable=True),
        sa.Column("fecha_real", sa.Date(), nullable=True),
    )

    # --- fotos ---
    op.create_table(
        "fotos",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "contrato_obra_id",
            sa.Integer(),
            sa.ForeignKey("contratos_obra.id"),
            nullable=False,
        ),
        sa.Column("archivo_nombre", sa.String(500), nullable=False),
        sa.Column("archivo_path", sa.String(1000), nullable=False),
        sa.Column("archivo_size_bytes", sa.Integer(), nullable=False),
        sa.Column("pie_de_foto", sa.Text(), nullable=True),
        sa.Column(
            "tipo",
            sa.Enum("avance", "sst", "ambiental", "social", "general", name="tipofoto"),
            server_default=sa.text("'general'"),
            nullable=False,
        ),
        sa.Column("fecha_toma", sa.Date(), nullable=False),
        sa.Column("latitud", sa.Numeric(10, 7), nullable=True),
        sa.Column("longitud", sa.Numeric(10, 7), nullable=True),
        sa.Column(
            "subido_por_id",
            sa.Integer(),
            sa.ForeignKey("usuarios.id"),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )

    # --- informes_semanales ---
    op.create_table(
        "informes_semanales",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "contrato_obra_id",
            sa.Integer(),
            sa.ForeignKey("contratos_obra.id"),
            nullable=False,
        ),
        sa.Column("numero_informe", sa.Integer(), nullable=False),
        sa.Column("semana_inicio", sa.Date(), nullable=False),
        sa.Column("semana_fin", sa.Date(), nullable=False),
        sa.Column(
            "estado",
            sa.Enum("borrador", "en_revision", "aprobado", "radicado", name="estadoinforme"),
            server_default=sa.text("'borrador'"),
            nullable=False,
        ),
        # S2 indicators
        sa.Column("avance_fisico_programado", sa.Numeric(5, 2), server_default=sa.text("0"), nullable=False),
        sa.Column("avance_fisico_ejecutado", sa.Numeric(5, 2), server_default=sa.text("0"), nullable=False),
        sa.Column("valor_acumulado_programado", sa.Numeric(18, 2), server_default=sa.text("0"), nullable=False),
        sa.Column("valor_acumulado_ejecutado", sa.Numeric(18, 2), server_default=sa.text("0"), nullable=False),
        # S3
        sa.Column("situaciones_problematicas", sa.Text(), nullable=True),
        # S5
        sa.Column("actividades_no_previstas", sa.Text(), nullable=True),
        sa.Column("actividades_no_previstas_narrativa", sa.Text(), nullable=True),
        # S6
        sa.Column("comentario_tecnico", sa.Text(), nullable=True),
        sa.Column("comentario_sst", sa.Text(), nullable=True),
        sa.Column("comentario_ambiental", sa.Text(), nullable=True),
        sa.Column("comentario_social", sa.Text(), nullable=True),
        # State transition timestamps
        sa.Column("fecha_envio_revision", sa.DateTime(timezone=True), nullable=True),
        sa.Column("fecha_aprobacion", sa.DateTime(timezone=True), nullable=True),
        sa.Column("fecha_radicacion", sa.DateTime(timezone=True), nullable=True),
        sa.Column(
            "aprobado_por_id",
            sa.Integer(),
            sa.ForeignKey("usuarios.id"),
            nullable=True,
        ),
        # Audit
        sa.Column(
            "creado_por_id",
            sa.Integer(),
            sa.ForeignKey("usuarios.id"),
            nullable=True,
        ),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )

    # --- snapshot_hitos ---
    op.create_table(
        "snapshot_hitos",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "informe_semanal_id",
            sa.Integer(),
            sa.ForeignKey("informes_semanales.id"),
            nullable=False,
        ),
        sa.Column(
            "hito_id",
            sa.Integer(),
            sa.ForeignKey("hitos.id"),
            nullable=False,
        ),
        sa.Column("numero", sa.Integer(), nullable=False),
        sa.Column("descripcion", sa.Text(), nullable=False),
        sa.Column("fecha_programada", sa.Date(), nullable=False),
        sa.Column("fecha_real", sa.Date(), nullable=True),
        sa.Column(
            "estado",
            sa.Enum("no_iniciado", "en_proceso", "cumplido", "vencido", name="estadohito", create_type=False),
            nullable=False,
        ),
        sa.Column("avance_porcentaje", sa.Numeric(5, 2), nullable=False),
        sa.Column("dias_retraso", sa.Integer(), server_default=sa.text("0"), nullable=False),
    )

    # --- informe_fotos ---
    op.create_table(
        "informe_fotos",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "informe_semanal_id",
            sa.Integer(),
            sa.ForeignKey("informes_semanales.id"),
            nullable=False,
        ),
        sa.Column(
            "foto_id",
            sa.Integer(),
            sa.ForeignKey("fotos.id"),
            nullable=False,
        ),
        sa.Column("orden", sa.Integer(), server_default=sa.text("0"), nullable=False),
        sa.Column("pie_de_foto_override", sa.Text(), nullable=True),
    )

    # --- acciones_plan ---
    op.create_table(
        "acciones_plan",
        sa.Column("id", sa.Integer(), primary_key=True),
        sa.Column(
            "informe_origen_id",
            sa.Integer(),
            sa.ForeignKey("informes_semanales.id"),
            nullable=False,
        ),
        sa.Column("numero", sa.Integer(), nullable=False),
        sa.Column("actividad", sa.Text(), nullable=False),
        sa.Column("responsable", sa.String(255), nullable=False),
        sa.Column(
            "responsable_usuario_id",
            sa.Integer(),
            sa.ForeignKey("usuarios.id"),
            nullable=True,
        ),
        sa.Column("fecha_programada", sa.Date(), nullable=False),
        sa.Column("fecha_cumplimiento", sa.Date(), nullable=True),
        sa.Column(
            "estado",
            sa.Enum("pendiente", "en_proceso", "cumplido", "vencido", name="estadoplanaccion"),
            server_default=sa.text("'pendiente'"),
            nullable=False,
        ),
        sa.Column("observaciones", sa.Text(), nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.text("now()"),
            nullable=False,
        ),
    )


def downgrade() -> None:
    op.drop_table("acciones_plan")
    op.drop_table("informe_fotos")
    op.drop_table("snapshot_hitos")
    op.drop_table("informes_semanales")
    op.drop_table("fotos")
    op.drop_table("actividades_no_previstas")
    op.drop_table("hitos")
    op.drop_table("contratos_obra")
    op.drop_table("contratos_interventoria")
    op.drop_table("usuarios")

    # Drop enums
    sa.Enum(name="rolusuario").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="estadohito").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="tipofoto").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="estadoinforme").drop(op.get_bind(), checkfirst=True)
    sa.Enum(name="estadoplanaccion").drop(op.get_bind(), checkfirst=True)
