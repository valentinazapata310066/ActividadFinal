# ActividadFinal — Rama `ops`

> **Sistema de Reservas de Espacios Institucionales**  
> Rama de operaciones — estructura base y configuración de despliegue.

[![Python](https://img.shields.io/badge/Python-3.12-blue)](https://www.python.org/) [![FastAPI](https://img.shields.io/badge/FastAPI-0.136.3-green)](https://fastapi.tiangolo.com/) [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)](https://www.postgresql.org/) [![Docker](https://img.shields.io/badge/Docker-Compose-2496ED)](https://docs.docker.com/compose/)

---

## Descripción general

Esta rama contiene la **estructura base y la configuración de despliegue** del sistema. Incluye los Dockerfiles, docker-compose.yml y la arquitectura inicial del backend con FastAPI, modelos SQLAlchemy y autenticación JWT.

---

## Estructura del repositorio
ActividadFinal-ops/
├── backend/
│ ├── app/
│ │ ├── api/
│ │ │ ├── init.py
│ │ │ ├── auth.py
│ │ │ ├── espacios.py
│ │ │ ├── reservas.py
│ │ │ └── usuarios.py
│ │ ├── crud/

│ │ │ ├── init.py
│ │ │ ├── espacio.py
│ │ │ ├── reserva.py
│ │ │ └── usuarios.py
│ │ ├── models/
│ │ │ ├── init.py
│ │ │ ├── espacio.py
│ │ │ ├── reserva.py
│ │ │ └── usuarios.py
│ │ ├── schemas/
│ │ │ ├── init.py
│ │ │ ├── auth.py
│ │ │ ├── espacio.py
│ │ │ ├── reserva.py
│ │ │ └── usuarios.py
│ │ ├── services/
│ │ │ ├── init.py
│ │ │ └── auth_service.py
│ │ ├── db.py
│ │ └── main.py
│ ├── .dockerignore
│ ├── Dockerfile
│ └── requirements.txt
├── frontend/
│ ├── css/
│ │ └── style.css
│ ├── js/
│ │ ├── api.js
│ │ ├── admin.js
│ │ ├── login.js
│ │ └── usuario.js
│ ├── index.html
│ ├── login.html
│ ├── admin.html
│ ├── usuario.html
│ └── Dockerfile
├── docker-compose.yml
└── .gitignore

text

---

## Tecnologías y dependencias

| Tecnología | Versión | Uso |
|---|---|---|
| Python | 3.12 | Lenguaje backend |
| FastAPI | 0.136.3 | Framework web |
| PostgreSQL | 15 | Base de datos |
| Docker | — | Contenedorización |
| Docker Compose | 3.8 | Orquestación |
| Nginx | Alpine | Servidor frontend |

---

## Variables de entorno

Crear archivo `.env` en la raíz:

```env
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=reservas_db
DATABASE_URL=postgresql://postgres:postgres@db:5432/reservas_db
SECRET_KEY=tu_clave_secreta
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
Instalación y ejecución
bash
# 1. Clonar el repositorio
git clone https://github.com/valentinazapata310066/ActividadFinal.git
cd ActividadFinal
git checkout ops

# 2. Crear archivo .env
cp .env.example .env

# 3. Levantar los servicios
docker compose up --build

# 4. Detener
docker compose down
Servicios y puertos
Servicio	Contenedor	Puerto
Base de datos	reservas_db	interno
Backend API	reservas_backend	8000
Frontend	reservas_frontend	80
Frontend: http://localhost

API Docs: http://localhost:8000/docs

Modelos de datos
Usuarios (tabla: usuarios)
id_usuario (PK)

nombre

correo (unique)

password_hash

rol (admin/usuario)

activo

Espacio (tabla: espacio)
id_espacio (PK)

nombre

ubicacion

capacidad

estado

Reserva (tabla: reservas)
id_reserva (PK)

id_usuario (FK → usuario)

id_espacio (FK → espacio)

fecha

hora_inicio

hora_fin

cantidad_asistentes

estado

Endpoints principales
Método	Ruta	Descripción
POST	/auth/token	Login JWT
POST	/usuario/registro	Registro público
GET	/usuario/me	Perfil propio
GET	/espacios/	Listar espacios
POST	/reservas/	Crear reserva
GET	/reservas/	Listar reservas
PATCH	/reservas/{id}/estado	Cambiar estado (admin)
Licencia
Proyecto académico - Tecnología en Desarrollo de Software