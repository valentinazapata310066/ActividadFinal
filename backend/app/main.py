from app.api import usuarios
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import Base, engine
from app.api import auth, usuarios, espacios, reservas

from app.db import Base, engine, SessionLocal
from app.api import auth, espacios, reservas
from app.models.usuarios import Usuarios
from app.services.auth_service import hashear_password

Base.metadata.create_all(bind=engine)

def crear_admin_inicial():
    db = SessionLocal()
    try:
        admin = db.query(Usuarios).filter(Usuarios.correo == "admin@test.com").first()
        if not admin:
            nuevo_admin = Usuarios(
                nombre="Administrador",
                correo="admin@test.com",
                password_hash=hashear_password("admin123"),
                rol="admin",
                activo=True
            )
            db.add(nuevo_admin)
            db.commit()
            print("✅ Admin inicial creado")
    finally:
        db.close()

crear_admin_inicial()

app = FastAPI(
    title="Sistema de Reservas de Espacios Institucionales",
    description="API para gestión de reservas con autenticación JWT y control de acceso por roles",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(usuarios.router)
app.include_router(espacios.router)
app.include_router(reservas.router)

@app.get("/", tags=["Health"])
def health_check():
    return {"status": "ok", "mensaje": "API de Reservas en línea"}