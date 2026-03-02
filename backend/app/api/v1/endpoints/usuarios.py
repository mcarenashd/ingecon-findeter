from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.deps import get_current_user, require_roles
from app.core.security import get_password_hash
from app.models.usuario import RolUsuario, Usuario
from app.schemas.usuario import UsuarioCreate, UsuarioResponse, UsuarioUpdate

router = APIRouter(prefix="/usuarios", tags=["Usuarios"])


@router.get("", response_model=list[UsuarioResponse])
def listar_usuarios(
    db: Session = Depends(get_db),
    _current_user: Usuario = Depends(get_current_user),
):
    return db.query(Usuario).order_by(Usuario.nombre_completo).all()


@router.post("", response_model=UsuarioResponse, status_code=status.HTTP_201_CREATED)
def crear_usuario(
    data: UsuarioCreate,
    db: Session = Depends(get_db),
    _current_user: Usuario = Depends(require_roles(RolUsuario.DIRECTOR)),
):
    existente = db.query(Usuario).filter(Usuario.email == data.email).first()
    if existente:
        raise HTTPException(
            status_code=400,
            detail="Ya existe un usuario con ese email",
        )

    usuario = Usuario(
        email=data.email,
        nombre_completo=data.nombre_completo,
        hashed_password=get_password_hash(data.password),
        rol=data.rol,
    )
    db.add(usuario)
    db.commit()
    db.refresh(usuario)
    return usuario


@router.get("/{usuario_id}", response_model=UsuarioResponse)
def obtener_usuario(
    usuario_id: int,
    db: Session = Depends(get_db),
    _current_user: Usuario = Depends(get_current_user),
):
    usuario = db.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return usuario


@router.patch("/{usuario_id}", response_model=UsuarioResponse)
def actualizar_usuario(
    usuario_id: int,
    data: UsuarioUpdate,
    db: Session = Depends(get_db),
    _current_user: Usuario = Depends(require_roles(RolUsuario.DIRECTOR)),
):
    usuario = db.get(Usuario, usuario_id)
    if not usuario:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")

    update_data = data.model_dump(exclude_unset=True)

    # Si viene password, hashear y mapear a hashed_password
    if "password" in update_data:
        password = update_data.pop("password")
        if password:
            update_data["hashed_password"] = get_password_hash(password)

    # Validar email único si cambió
    if "email" in update_data and update_data["email"] != usuario.email:
        existente = db.query(Usuario).filter(Usuario.email == update_data["email"]).first()
        if existente:
            raise HTTPException(
                status_code=400,
                detail="Ya existe un usuario con ese email",
            )

    for field, value in update_data.items():
        setattr(usuario, field, value)

    db.commit()
    db.refresh(usuario)
    return usuario
