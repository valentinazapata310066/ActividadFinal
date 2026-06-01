from pydantic import BaseModel
from typing import Optional

class UsuarioCrear(BaseModel):
    nombre: str
    correo: str
    password: str
    rol: str = "usuario"

class UsuarioRespuesta(BaseModel):
    id_usuario: int
    nombre: str
    correo: str
    rol: str
    activo: bool

    model_config = {"from_attributes": True}

class UsuarioActualizar(BaseModel):
    nombre: Optional[str] = None
    correo: Optional[str] = None
    rol: Optional[str] = None
    activo: Optional[bool] = None

class UsuarioLogin(BaseModel):
    correo: str
    password: str