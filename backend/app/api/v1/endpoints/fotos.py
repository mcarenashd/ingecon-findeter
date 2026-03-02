import os
import uuid
from datetime import date

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile, status
from fastapi.responses import FileResponse
from sqlalchemy.orm import Session

from app.core.config import settings
from app.core.database import get_db
from app.models.contrato import ContratoObra
from app.models.foto import Foto, TipoFoto
from app.schemas.foto import FotoResponse

router = APIRouter(prefix="/fotos", tags=["Fotos"])


@router.post(
    "/upload",
    response_model=FotoResponse,
    status_code=status.HTTP_201_CREATED,
)
async def subir_foto(
    contrato_obra_id: int = Form(...),
    fecha_toma: date = Form(...),
    file: UploadFile = File(...),
    pie_de_foto: str | None = Form(None),
    tipo: TipoFoto = Form(TipoFoto.GENERAL),
    latitud: float | None = Form(None),
    longitud: float | None = Form(None),
    db: Session = Depends(get_db),
):
    # Validar contrato
    contrato = db.get(ContratoObra, contrato_obra_id)
    if not contrato:
        raise HTTPException(status_code=404, detail="Contrato de obra no encontrado")

    # Validar tipo de archivo
    if file.content_type not in settings.ALLOWED_IMAGE_TYPES:
        raise HTTPException(
            status_code=400,
            detail=f"Tipo de archivo no permitido: {file.content_type}. "
            f"Permitidos: {settings.ALLOWED_IMAGE_TYPES}",
        )

    # Leer contenido
    content = await file.read()
    if len(content) > settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail=f"Archivo excede el tamaño máximo de {settings.MAX_UPLOAD_SIZE_MB}MB",
        )

    # Guardar archivo
    ext = os.path.splitext(file.filename or "foto.jpg")[1]
    unique_name = f"{uuid.uuid4().hex}{ext}"
    rel_path = f"contratos/{contrato_obra_id}/{unique_name}"
    abs_path = os.path.join(settings.UPLOAD_DIR, rel_path)

    os.makedirs(os.path.dirname(abs_path), exist_ok=True)
    with open(abs_path, "wb") as f:
        f.write(content)

    # Crear registro
    from decimal import Decimal

    foto = Foto(
        contrato_obra_id=contrato_obra_id,
        archivo_nombre=file.filename or unique_name,
        archivo_path=rel_path,
        archivo_size_bytes=len(content),
        pie_de_foto=pie_de_foto,
        tipo=tipo,
        fecha_toma=fecha_toma,
        latitud=Decimal(str(latitud)) if latitud is not None else None,
        longitud=Decimal(str(longitud)) if longitud is not None else None,
    )
    db.add(foto)
    db.commit()
    db.refresh(foto)
    return foto


@router.get("", response_model=list[FotoResponse])
def listar_fotos(
    contrato_obra_id: int,
    fecha_desde: date | None = None,
    fecha_hasta: date | None = None,
    tipo: TipoFoto | None = None,
    db: Session = Depends(get_db),
):
    query = db.query(Foto).filter(Foto.contrato_obra_id == contrato_obra_id)
    if fecha_desde:
        query = query.filter(Foto.fecha_toma >= fecha_desde)
    if fecha_hasta:
        query = query.filter(Foto.fecha_toma <= fecha_hasta)
    if tipo:
        query = query.filter(Foto.tipo == tipo)
    return query.order_by(Foto.fecha_toma.desc(), Foto.id.desc()).all()


@router.get("/{foto_id}", response_model=FotoResponse)
def obtener_foto(foto_id: int, db: Session = Depends(get_db)):
    foto = db.get(Foto, foto_id)
    if not foto:
        raise HTTPException(status_code=404, detail="Foto no encontrada")
    return foto


@router.get("/{foto_id}/archivo")
def descargar_archivo_foto(foto_id: int, db: Session = Depends(get_db)):
    foto = db.get(Foto, foto_id)
    if not foto:
        raise HTTPException(status_code=404, detail="Foto no encontrada")

    abs_path = os.path.join(settings.UPLOAD_DIR, foto.archivo_path)
    if not os.path.exists(abs_path):
        raise HTTPException(status_code=404, detail="Archivo no encontrado en disco")

    return FileResponse(abs_path, filename=foto.archivo_nombre)


@router.delete("/{foto_id}", status_code=status.HTTP_204_NO_CONTENT)
def eliminar_foto(foto_id: int, db: Session = Depends(get_db)):
    foto = db.get(Foto, foto_id)
    if not foto:
        raise HTTPException(status_code=404, detail="Foto no encontrada")

    # No eliminar si está en un informe aprobado o radicado
    from app.models.informe import EstadoInforme, InformeFoto, InformeSemanal

    linked = (
        db.query(InformeFoto)
        .join(InformeSemanal)
        .filter(
            InformeFoto.foto_id == foto_id,
            InformeSemanal.estado.in_([EstadoInforme.APROBADO, EstadoInforme.RADICADO]),
        )
        .first()
    )
    if linked:
        raise HTTPException(
            status_code=400,
            detail="No se puede eliminar una foto vinculada a un informe aprobado o radicado",
        )

    # Eliminar archivo físico
    abs_path = os.path.join(settings.UPLOAD_DIR, foto.archivo_path)
    if os.path.exists(abs_path):
        os.remove(abs_path)

    db.delete(foto)
    db.commit()
