from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import date, time

class ReservaCrear(BaseModel):
    id_espacio: int
    fecha: date
    hora_inicio: time
    hora_fin: time
    cantidad_asistentes: int

    @field_validator("hora_fin")
    @classmethod
    def validar_horas(cls, hora_fin, info):
        hora_inicio = info.data.get("hora_inicio")
        if hora_inicio and hora_fin <= hora_inicio:
            raise ValueError("La hora de fin debe ser mayor a la hora de inicio")
        return hora_fin

class ReservaRespuesta(BaseModel):
    id_reserva: int
    id_usuario: int
    id_espacio: int
    fecha: date
    hora_inicio: time
    hora_fin: time
    cantidad_asistentes: int
    estado: str

    model_config = {"from_attributes": True}

class ReservaActualizar(BaseModel):
    estado: Optional[str] = None