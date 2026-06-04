from sqlalchemy.orm import Session
from app.models.espacio import Espacio
from app.schemas.espacio import EspacioCrear, EspacioActualizar

def crear(db: Session, datos: EspacioCrear):
    nuevo = Espacio(
        nombre=datos.nombre,
        ubicacion=datos.ubicacion,
        capacidad=datos.capacidad,
        estado=datos.estado
    )
    db.add(nuevo)
    db.commit()
    db.refresh(nuevo)
    return nuevo

def listar(db: Session):
    return db.query(Espacio).all()

def listar_disponibles(db: Session):
    return db.query(Espacio).filter(Espacio.estado == "disponible").all()

def obtener_por_id(db: Session, id_espacio: int):
    return db.query(Espacio).filter(Espacio.id_espacio == id_espacio).first()

def actualizar(db: Session, id_espacio: int, datos: EspacioActualizar):
    espacio = obtener_por_id(db, id_espacio)
    if not espacio:
        return None
    
    if datos.nombre is not None:
        espacio.nombre = datos.nombre
    if datos.ubicacion is not None:
        espacio.ubicacion = datos.ubicacion
    if datos.capacidad is not None:
        espacio.capacidad = datos.capacidad
    if datos.estado is not None:
        espacio.estado = datos.estado
    
    db.commit()
    db.refresh(espacio)
    return espacio

def eliminar(db: Session, id_espacio: int):
    espacio = obtener_por_id(db, id_espacio)
    if not espacio:
        return None
    db.delete(espacio)
    db.commit()
    return espacio