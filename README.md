# ActividadFinal — Rama `ops`

> **Sistema de Reservas de Espacios Institucionales**  
> Aplicación web completa con backend FastAPI, frontend HTML/JS y base de datos PostgreSQL, desplegada con Docker.

[![Python](https://img.shields.io/badge/Python-3.12-blue)](https://www.python.org/) [![FastAPI](https://img.shields.io/badge/FastAPI-0.136.3-green)](https://fastapi.tiangolo.com/) [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)](https://www.postgresql.org/) [![Docker](https://img.shields.io/badge/Docker-Compose-2496ED)](https://docs.docker.com/compose/)

---

## Descripción general

Sistema web para gestionar reservas de espacios institucionales. Permite a usuarios crear reservas y a administradores gestionar espacios y aprobar o rechazar solicitudes. Implementa autenticación JWT, control de acceso por roles y reglas de negocio completas.

---

## Estado de implementación

| Componente | Estado |
|---|---|
| Docker Compose + Dockerfiles | ✅ Completo |
| Backend: estructura de carpetas | ✅ Completo |
| Backend: `main.py` | ✅ Funcional con creación de admin inicial |
| Backend: modelos SQLAlchemy | ✅ Completos |
| Backend: schemas Pydantic | ✅ Completos |
| Backend: `auth_service.py` | ✅ Funcional |
| Backend: `api/auth.py` | ✅ Funcional |
| Backend: `api/espacios.py` | ✅ Funcional |
| Backend: `api/reservas.py` | ✅ Funcional con validaciones de negocio completas |
| Backend: `api/usuarios.py` | ✅ Funcional |
| Backend: `crud/espacio.py` | ✅ Implementado |
| Backend: `crud/reserva.py` | ✅ Implementado con reglas de negocio |
| Backend: `crud/usuarios.py` | ✅ Implementado |
| Frontend: `login.html` | ✅ Login completo con JWT |
| Frontend: `js/login.js` | ✅ Conexión real al backend |
| Frontend: `admin.html` | ✅ Implementado |
| Frontend: `usuario.html` | ✅ Implementado |
| Frontend: `js/admin.js` | ✅ Conectado al backend |
| Frontend: `js/usuario.js` | ✅ Conectado al backend |
| Frontend: `js/api.js` | ✅ Implementado |
| Frontend: `dashboard.html` | ✅ Panel dinámico por rol |

---

## Tabla de contenidos

- [Estructura del repositorio](#estructura-del-repositorio)
- [Tecnologías y dependencias](#tecnologías-y-dependencias)
- [Variables de entorno](#variables-de-entorno)
- [Instalación y ejecución](#instalación-y-ejecución)
- [Servicios y puertos](#servicios-y-puertos)
- [Arquitectura del backend](#arquitectura-del-backend)
- [Modelos de datos](#modelos-de-datos)
- [Endpoints de la API](#endpoints-de-la-api)
- [Archivos ignorados](#archivos-ignorados)

---

## Estructura del repositorio

```
ActividadFinal-ops/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py          ✅ Endpoint de login / token JWT
│   │   │   ├── espacios.py      ✅ CRUD de espacios
│   │   │   ├── reservas.py      ✅ Endpoints reservas con validaciones
│   │   │   └── usuarios.py      ✅ CRUD de usuarios
│   │   ├── crud/
│   │   │   ├── espacio.py       ✅ Implementado
│   │   │   ├── reserva.py       ✅ Implementado con reglas de negocio
│   │   │   └── usuarios.py      ✅ Implementado
│   │   ├── models/
│   │   │   ├── espacio.py       ✅ Modelo: Espacio
│   │   │   ├── reserva.py       ✅ Modelo: Reserva
│   │   │   └── usuarios.py      ✅ Modelo: Usuarios
│   │   ├── schemas/
│   │   │   ├── auth.py          ✅ Schemas: Login, Token
│   │   │   ├── espacio.py       ✅ Schemas: Espacio
│   │   │   ├── reserva.py       ✅ Schemas: Reserva
│   │   │   └── usuarios.py      ✅ Schemas: Usuario
│   │   ├── services/
│   │   │   └── auth_service.py  ✅ JWT, hashing, guards
│   │   ├── db.py                ✅ Conexión SQLAlchemy
│   │   └── main.py              ✅ App FastAPI con admin inicial
│   ├── .dockerignore
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── css/
│   │   └── style.css            ✅ Estilos base
│   ├── js/
│   │   ├── api.js               ✅ Implementado
│   │   ├── admin.js             ✅ Conectado al backend
│   │   ├── login.js             ✅ Login con JWT
│   │   └── usuario.js           ✅ Conectado al backend
│   ├── index.html               ✅ Selección de rol
│   ├── login.html               ✅ Formulario de login
│   ├── dashboard.html           ✅ Panel dinámico por rol
│   ├── admin.html               ✅ Panel administrador
│   └── usuario.html             ✅ Panel usuario
├── docker-compose.yml
└── .gitignore
```

---

## Tecnologías y dependencias

### Backend

| Paquete | Versión | Uso |
|---|---|---|
| `fastapi` | 0.136.3 | Framework web / API REST |
| `uvicorn` | 0.48.0 | Servidor ASGI |
| `sqlalchemy` | 2.0.50 | ORM para PostgreSQL |
| `psycopg2-binary` | 2.9.12 | Driver PostgreSQL |
| `pydantic` | 2.13.4 | Validación de datos / schemas |
| `python-jose` | 3.5.0 | Generación y verificación de JWT |
| `passlib` + `bcrypt` | 1.7.4 / 4.0.1 | Hash seguro de contraseñas |
| `python-dotenv` | 1.2.2 | Carga de variables de entorno |
| `python-multipart` | 0.0.29 | Soporte para formularios OAuth2 |
| `email-validator` | 2.3.0 | Validación de emails |

### Frontend

| Tecnología | Uso |
|---|---|
| HTML5 | Estructura de páginas |
| CSS3 | Estilos y diseño responsivo |
| JavaScript (Vanilla) | Lógica del cliente |
| Nginx (Alpine) | Servidor web para archivos estáticos |

### Infraestructura

| Tecnología | Versión | Uso |
|---|---|---|
| Docker | — | Contenedorización |
| Docker Compose | 3.8 | Orquestación de servicios |
| PostgreSQL | 15 | Base de datos relacional |

---

## Variables de entorno

Crear un archivo `.env` en la raíz del proyecto:

```env
# Base de datos PostgreSQL
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
POSTGRES_DB=reservas_db

# Conexión que usa el backend
DATABASE_URL=postgresql://postgres:postgres@db:5432/reservas_db

# Seguridad JWT
SECRET_KEY=una-clave-secreta-muy-larga-y-segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## Instalación y ejecución

### Requisitos previos

- [Docker](https://docs.docker.com/get-docker/) v20+
- [Docker Compose](https://docs.docker.com/compose/install/) v2+

### Pasos

```bash
# 1. Clonar el repositorio y cambiar a la rama ops
git clone https://github.com/valentinazapata310066/ActividadFinal.git
cd ActividadFinal
git checkout ops

# 2. Crear el archivo .env con los valores indicados arriba

# 3. Construir y levantar los servicios
docker compose up --build

# En segundo plano:
docker compose up --build -d

# 4. Detener
docker compose down

# Eliminar también los datos:
docker compose down -v
```

---

## Servicios y puertos

| Servicio | Contenedor | Puerto | Descripción |
|---|---|---|---|
| `db` | `reservas_db` | interno | PostgreSQL 15 |
| `backend` | `reservas_backend` | `8000` | API FastAPI |
| `frontend` | `reservas_frontend` | `80` | Interfaz Nginx |

- **Frontend:** http://localhost
- **API:** http://localhost:8000
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Red y volúmenes

- **Red:** `reservas_network` (tipo `bridge`)
- **Volumen:** `postgres_data`

---

## Arquitectura del backend

```
main.py
  └── Crea tablas (Base.metadata.create_all)
  └── Crea admin inicial (admin@test.com / admin123)
  └── Configura CORS (allow_origins=["*"])
  └── Registra routers: /auth, /usuarios, /espacios, /reservas

db.py
  └── Lee DATABASE_URL desde .env
  └── Crea engine SQLAlchemy
  └── Expone get_db() como dependencia inyectable

services/auth_service.py
  └── hashear_password / verificar_password (bcrypt)
  └── crear_token (JWT HS256)
  └── get_usuario_actual
  └── get_admin_actual
```

---

## Modelos de datos

### Usuarios (`tabla: usuarios`)

| Campo | Tipo | Descripción |
|---|---|---|
| `id_usuario` | Integer (PK) | Identificador único |
| `nombre` | String | Nombre completo |
| `correo` | String (unique) | Email / credencial de login |
| `password_hash` | String | Contraseña hasheada con bcrypt |
| `rol` | String | `"admin"` o `"usuario"` |
| `activo` | Boolean | Si la cuenta está habilitada |

### Espacio (`tabla: espacios`)

| Campo | Tipo | Descripción |
|---|---|---|
| `id_espacio` | Integer (PK) | Identificador único |
| `nombre` | String | Nombre del espacio |
| `ubicacion` | String | Ubicación física |
| `capacidad` | Integer | Aforo máximo de personas |
| `estado` | String | `"disponible"`, `"inactivo"`, `"en mantenimiento"` |

### Reserva (`tabla: reservas`)

| Campo | Tipo | Descripción |
|---|---|---|
| `id_reserva` | Integer (PK) | Identificador único |
| `id_usuario` | Integer (FK → usuarios) | Usuario que reservó |
| `id_espacio` | Integer (FK → espacios) | Espacio reservado |
| `fecha` | Date | Fecha de la reserva |
| `hora_inicio` | Time | Hora de inicio |
| `hora_fin` | Time | Hora de finalización |
| `cantidad_asistentes` | Integer | Número de asistentes |
| `estado` | String | `"esperando"`, `"aprobada"`, `"rechazada"` |

---

## Endpoints de la API

### Autenticación — `/auth`

| Método | Ruta | Acceso | Descripción |
|---|---|---|---|
| POST | `/auth/token` | Público | Login — devuelve JWT Bearer token |

### Usuarios — `/usuarios`

| Método | Ruta | Acceso | Descripción |
|---|---|---|---|
| POST | `/usuarios/` | Admin | Crear usuario |
| POST | `/usuarios/registro` | Público | Registro libre |
| GET | `/usuarios/` | Admin | Listar usuarios |
| GET | `/usuarios/me` | Autenticado | Ver perfil propio |
| GET | `/usuarios/{id}` | Admin | Ver usuario por ID |
| PATCH | `/usuarios/{id}` | Admin | Actualizar usuario |

### Espacios — `/espacios`

| Método | Ruta | Acceso | Descripción |
|---|---|---|---|
| POST | `/espacios/` | Admin | Crear espacio |
| GET | `/espacios/` | Autenticado | Listar espacios |
| GET | `/espacios/{id}` | Autenticado | Ver espacio por ID |
| PATCH | `/espacios/{id}` | Admin | Actualizar espacio |
| DELETE | `/espacios/{id}` | Admin | Eliminar espacio |

### Reservas — `/reservas`

| Método | Ruta | Acceso | Descripción |
|---|---|---|---|
| POST | `/reservas/` | Autenticado | Crear reserva |
| GET | `/reservas/` | Autenticado | Listar reservas |
| GET | `/reservas/{id}` | Autenticado | Ver reserva por ID |
| PATCH | `/reservas/{id}/estado` | Admin | Cambiar estado |
| DELETE | `/reservas/{id}` | Autenticado | Cancelar reserva |

---

## Credenciales iniciales

Al arrancar la aplicación se crea automáticamente un usuario administrador:

| Campo | Valor |
|---|---|
| Correo | `admin@test.com` |
| Contraseña | `admin123` |

---

## Archivos ignorados

```gitignore
desktop.ini
venv/
__pycache__/
.env
*.pyc
```