from pydantic import BaseModel, EmailStr

from app.models.usuario import RolUsuario


class UsuarioBase(BaseModel):
    email: str
    nombre_completo: str
    rol: RolUsuario


class UsuarioCreate(UsuarioBase):
    password: str


class UsuarioResponse(UsuarioBase):
    id: int
    activo: bool

    model_config = {"from_attributes": True}


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str
    role: str
