from app.api import usuarios
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import Base, engine
from app.api import auth, espacios, reservas

Base.metadata.create_all(bind=engine)

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