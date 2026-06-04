# ActividadFinal — Rama `ops`

> **Sistema de Reservas de Espacios Institucionales**  
> Rama de operaciones inicial — estructura base y scaffolding, código en proceso de desarrollo.

[![Python](https://img.shields.io/badge/Python-3.12-blue)](https://www.python.org/) [![FastAPI](https://img.shields.io/badge/FastAPI-0.136.3-green)](https://fastapi.tiangolo.com/) [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)](https://www.postgresql.org/) [![Docker](https://img.shields.io/badge/Docker-Compose-2496ED)](https://docs.docker.com/compose/)

---

## Descripción general

Esta rama representa el **estado inicial del proyecto**: la estructura de carpetas, los archivos de configuración e infraestructura (Docker, docker-compose) y la base del backend están definidos, pero una parte importante de la lógica de negocio aún no está implementada. Varios archivos de la capa `crud/` están vacíos y el frontend apenas tiene el esqueleto de login.

Es el punto de partida desde el que se desarrollaron las ramas `dev` y `main`.

---

## Estado de implementación

| Componente | Estado |
|---|---|
| Docker Compose + Dockerfiles | ✅ Completo |
| Backend: estructura de carpetas | ✅ Completo |
| Backend: `main.py` | ✅ Funcional (sin creación de admin inicial) |
| Backend: modelos SQLAlchemy | ✅ Definidos (con diferencias respecto a `main`) |
| Backend: schemas Pydantic | ✅ Completos |
| Backend: `auth_service.py` | ✅ Funcional |
| Backend: `api/auth.py` | ✅ Funcional |
| Backend: `api/espacios.py` | ✅ Funcional |
| Backend: `api/reservas.py` | ⚠️ Funcional pero sin validaciones de negocio |
| Backend: `api/usuarios.py` | ✅ Funcional |
| Backend: `crud/espacio.py` | ❌ Vacío (sin implementar) |
| Backend: `crud/reserva.py` | ❌ Vacío (sin implementar) |
| Backend: `crud/usuarios.py` | ❌ Vacío (sin implementar) |
| Frontend: `login.html` | ✅ Estructura completa |
| Frontend: `js/login.js` | ⚠️ Stub — sin conexión real al backend |
| Frontend: `admin.html` | ❌ Vacío |
| Frontend: `usuario.html` | ❌ Vacío |
| Frontend: `js/admin.js` | ❌ Vacío |
| Frontend: `js/usuario.js` | ❌ Vacío |
| Frontend: `js/api.js` | ❌ Vacío |
| Frontend: `dashboard.html` | ❌ No existe en esta rama |

---

## Diferencias clave respecto a `main`

### Backend

| Aspecto | `ops` | `main` |
|---|---|---|
| Clase modelo usuario | `Usuarios` (plural) | `Usuario` (singular) |
| Tabla modelo usuario | `usuarios` | `usuarios` |
| PK de usuario en modelo | `id_usuarios` (plural) | `id_usuario` |
| FK en `Reserva` | `ForeignKey("usuario.id_usuario")` | `ForeignKey("usuarios.id_usuario")` |
| `crud/` | Archivos vacíos | Totalmente implementados |
| `main.py` | Sin creación de admin inicial | Crea admin `admin@test.com` al arrancar |
| Validaciones en reservas | Sin validaciones de negocio | Validaciones completas (24h, horarios, capacidad, solapamiento) |
| Endpoints extra en reservas | No existen `/mis-reservas` ni `/pendientes` | Ambos implementados |
| `SECRET_KEY` en auth_service | Sin valor por defecto (requiere `.env`) | Con valor por defecto fallback |
| Router usuarios | Prefijo `/usuario` | Prefijo `/usuarios` |

### Frontend

| Aspecto | `ops` | `main` |
|---|---|---|
| `index.html` | Redirección automática a `login.html` | Pantalla de selección de rol |
| `js/login.js` | Stub sin fetch real | Login completo con JWT y redirección |
| `admin.html` / `usuario.html` | Vacíos | Implementados con formularios |
| `js/admin.js` / `js/usuario.js` | Vacíos | Implementados |
| `dashboard.html` | No existe | Implementado |

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
- [Estado del frontend](#estado-del-frontend)
- [Archivos ignorados](#archivos-ignorados)

---

## Estructura del repositorio

```
ActividadFinal-ops/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py          # Endpoint de login / token JWT ✅
│   │   │   ├── espacios.py      # CRUD de espacios ✅
│   │   │   ├── reservas.py      # Endpoints reservas (sin validaciones) ⚠️
│   │   │   └── usuarios.py      # CRUD de usuarios ✅
│   │   ├── crud/
│   │   │   ├── espacio.py       # ❌ VACÍO
│   │   │   ├── reserva.py       # ❌ VACÍO
│   │   │   └── usuarios.py      # ❌ VACÍO
│   │   ├── models/
│   │   │   ├── espacio.py       # Modelo: Espacio ✅
│   │   │   ├── reserva.py       # Modelo: Reserva ✅
│   │   │   └── usuarios.py      # Modelo: Usuarios (clase plural) ✅
│   │   ├── schemas/
│   │   │   ├── auth.py          # Schemas: Login, Token ✅
│   │   │   ├── espacio.py       # Schemas: Espacio ✅
│   │   │   ├── reserva.py       # Schemas: Reserva ✅
│   │   │   └── usuarios.py      # Schemas: Usuario ✅
│   │   ├── services/
│   │   │   └── auth_service.py  # JWT, hashing, guards ✅
│   │   ├── db.py                # Conexión SQLAlchemy ✅
│   │   └── main.py              # App FastAPI (sin admin inicial) ✅
│   ├── .dockerignore
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── css/
│   │   └── style.css            # Estilos base ✅
│   ├── js/
│   │   ├── api.js               # ❌ VACÍO
│   │   ├── admin.js             # ❌ VACÍO
│   │   ├── login.js             # Stub sin conexión real ⚠️
│   │   └── usuario.js           # ❌ VACÍO
│   ├── index.html               # Redirige automáticamente a login.html ✅
│   ├── login.html               # Formulario de login ✅
│   ├── admin.html               # ❌ VACÍO
│   └── usuario.html             # ❌ VACÍO
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
| JavaScript (Vanilla) | Lógica del cliente (parcialmente implementada) |
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
POSTGRES_USER=tu_usuario
POSTGRES_PASSWORD=tu_contraseña_segura
POSTGRES_DB=reservas_db

# Conexión que usa el backend
DATABASE_URL=postgresql://tu_usuario:tu_contraseña_segura@db:5432/reservas_db

# Seguridad JWT — obligatorio (sin valor por defecto en esta rama)
SECRET_KEY=una-clave-secreta-muy-larga-y-segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> **Importante:** en esta rama `SECRET_KEY` **no tiene valor por defecto** en `auth_service.py`. Si no se define en `.env`, el servicio fallará al intentar generar tokens.

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
  └── NO crea admin inicial (diferencia con main/dev)
  └── Configura CORS (allow_origins=["*"])
  └── Registra routers: /auth, /usuario, /espacios, /reservas

db.py
  └── Lee DATABASE_URL desde .env
  └── Crea engine SQLAlchemy
  └── Expone get_db() como dependencia inyectable

services/auth_service.py
  └── hashear_password / verificar_password (bcrypt)
  └── crear_token (JWT HS256)
  └── get_usuario_actual — usa modelo Usuarios (plural)
  └── get_admin_actual
```

---

## Modelos de datos

### Usuarios (`tabla: usuarios`)

> **Nota:** en esta rama la clase se llama `Usuarios` (plural), a diferencia de `Usuario` en `main`/`dev`.

| Campo | Tipo | Descripción |
|---|---|---|
| `id_usuario` | Integer (PK) | Identificador único |
| `nombre` | String | Nombre completo |
| `correo` | String (unique) | Email / credencial de login |
| `password_hash` | String | Contraseña hasheada con bcrypt |
| `rol` | String | `"admin"` o `"usuario"` |
| `activo` | Boolean | Si la cuenta está habilitada |

### Espacio (`tabla: espacio`)

> **Nota:** la FK en `Reserva` apunta a `"espacio.id_espacio"` (singular), diferente a `"espacios.id_espacio"` en `main`.

| Campo | Tipo | Descripción |
|---|---|---|
| `id_espacio` | Integer (PK) | Identificador único |
| `nombre` | String | Nombre del espacio |
| `ubicacion` | String | Ubicación física |
| `capacidad` | Integer | Aforo máximo de personas |
| `estado` | String | `"disponible"`, `"inactivo"`, `"mantenimiento"` |

### Reserva (`tabla: reservas`)

| Campo | Tipo | Descripción |
|---|---|---|
| `id_reserva` | Integer (PK) | Identificador único |
| `id_usuario` | Integer (FK → usuario) | Usuario que reservó |
| `id_espacio` | Integer (FK → espacio) | Espacio reservado |
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

### Usuarios — `/usuario` ⚠️ (prefijo singular, diferente a `main`)

| Método | Ruta | Acceso | Descripción |
|---|---|---|---|
| POST | `/usuario/` | Admin | Crear usuario |
| POST | `/usuario/registro` | Público | Registro libre |
| GET | `/usuario/` | Admin | Listar usuarios |
| GET | `/usuario/me` | Autenticado | Ver perfil propio |
| GET | `/usuario/{id}` | Admin | Ver usuario por ID |
| PATCH | `/usuario/{id}` | Admin | Actualizar usuario |

> **Advertencia:** `crud/usuarios.py` está vacío. Estos endpoints fallarán si se invocan.

### Espacios — `/espacios`

| Método | Ruta | Acceso | Descripción |
|---|---|---|---|
| POST | `/espacios/` | Admin | Crear espacio |
| GET | `/espacios/` | Autenticado | Listar espacios |
| GET | `/espacios/{id}` | Autenticado | Ver espacio por ID |
| PATCH | `/espacios/{id}` | Admin | Actualizar espacio |
| DELETE | `/espacios/{id}` | Admin | Eliminar espacio |

> **Advertencia:** `crud/espacio.py` está vacío. Estos endpoints fallarán si se invocan.  
> **Nota:** no existe el endpoint `/espacios/disponibles` en esta rama.

### Reservas — `/reservas`

| Método | Ruta | Acceso | Descripción |
|---|---|---|---|
| POST | `/reservas/` | Autenticado | Crear reserva (sin validaciones de negocio) |
| GET | `/reservas/` | Autenticado | Listar reservas |
| GET | `/reservas/{id}` | Autenticado | Ver reserva por ID |
| PATCH | `/reservas/{id}/estado` | Admin | Cambiar estado (sin validación de valor) |
| DELETE | `/reservas/{id}` | Autenticado | Cancelar reserva |

> **Advertencia:** `crud/reserva.py` está vacío. Estos endpoints fallarán si se invocan.  
> **Nota:** no existen los endpoints `/reservas/mis-reservas` ni `/reservas/pendientes` en esta rama.

---

## Estado del frontend

### Páginas funcionales

- **`index.html`:** redirección automática (`meta refresh`) a `login.html`.
- **`login.html`:** formulario de login con campos de correo y contraseña. Vinculado a `js/login.js`.

### Páginas vacías (sin implementar)

- `admin.html` — sin contenido
- `usuario.html` — sin contenido

### JavaScript

- **`js/login.js`:** stub funcional. Valida que los campos no estén vacíos y muestra el mensaje `"Login pendiente de conexión con backend..."`. **No realiza ninguna llamada fetch al backend.**
- **`js/api.js`** — vacío
- **`js/admin.js`** — vacío
- **`js/usuario.js`** — vacío

### Estilos

- **`css/style.css`:** estilos base completos: layout centrado, `login-container`, inputs, botones, cards.

---

## Archivos ignorados

```gitignore
desktop.ini
venv/
__pycache__/
.env
*.pyc
```