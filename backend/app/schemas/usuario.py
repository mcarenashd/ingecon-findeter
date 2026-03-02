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


class UsuarioUpdate(BaseModel):
    email: str | None = None
    nombre_completo: str | None = None
    rol: RolUsuario | None = None
    activo: bool | None = None
    password: str | None = None


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenPayload(BaseModel):
    sub: str
    role: str
