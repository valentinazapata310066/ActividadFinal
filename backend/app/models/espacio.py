from sqlalchemy import Column, Integer, String
from app.db import Base

class Espacio(Base):
    __tablename__ = "espacios"

    id_espacio = Column(Integer, primary_key=True, index=True)
    nombre = Column(String, nullable=False)
    ubicacion = Column(String, nullable=False)
    capacidad = Column(Integer, nullable=False)
    estado = Column(String, nullable=False, default="disponible")