from pydantic import BaseModel
from typing import Optional

class EspacioCrear(BaseModel):
    nombre: str
    ubicacion: str
    capacidad: int
    estado: str = "disponible"

class EspacioRespuesta(BaseModel):
    id_espacio: int
    nombre: str
    ubicacion: str
    capacidad: int
    estado: str

    model_config = {"from_attributes": True}

class EspacioActualizar(BaseModel):
    nombre: Optional[str] = None
    ubicacion: Optional[str] = None
    capacidad: Optional[int] = None
    estado: Optional[str] = None