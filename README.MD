# ActividadFinal — Rama `main`

> **Sistema de Reservas de Espacios Institucionales**  
> Rama de producción — código estable y funcional completo.

[![Python](https://img.shields.io/badge/Python-3.12-blue)](https://www.python.org/) [![FastAPI](https://img.shields.io/badge/FastAPI-0.136.3-green)](https://fastapi.tiangolo.com/) [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)](https://www.postgresql.org/) [![Docker](https://img.shields.io/badge/Docker-Compose-2496ED)](https://docs.docker.com/compose/)

---

## Descripción general

Aplicación web fullstack para la gestión de reservas de espacios institucionales (salas, laboratorios, auditorios, etc.). Cuenta con autenticación JWT, control de acceso por roles (`admin` / `usuario`), validaciones de horario y disponibilidad, y un panel diferenciado para cada tipo de usuario.

El sistema se levanta completamente con Docker Compose: backend en Python/FastAPI, frontend estático servido por Nginx, y base de datos PostgreSQL 15.

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
- [Lógica de negocio y validaciones](#lógica-de-negocio-y-validaciones)
- [Autenticación y autorización](#autenticación-y-autorización)
- [Estructura del frontend](#estructura-del-frontend)
- [Flujo de uso de la aplicación](#flujo-de-uso-de-la-aplicación)
- [Usuario administrador inicial](#usuario-administrador-inicial)
- [Archivos ignorados](#archivos-ignorados)

---

## Estructura del repositorio

```
ActividadFinal-main/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   ├── __init__.py
│   │   │   ├── auth.py          # Endpoint de login / token JWT
│   │   │   ├── espacios.py      # CRUD de espacios (admin)
│   │   │   ├── reservas.py      # CRUD de reservas (usuario/admin)
│   │   │   └── usuarios.py      # CRUD de usuarios + registro público
│   │   ├── crud/
│   │   │   ├── espacio.py       # Operaciones DB para espacios
│   │   │   ├── reserva.py       # Operaciones DB para reservas
│   │   │   └── usuario.py       # Operaciones DB para usuarios
│   │   ├── models/
│   │   │   ├── espacio.py       # Modelo SQLAlchemy: Espacio
│   │   │   ├── reserva.py       # Modelo SQLAlchemy: Reserva
│   │   │   └── usuario.py       # Modelo SQLAlchemy: Usuario
│   │   ├── schemas/
│   │   │   ├── auth.py          # Schemas Pydantic: Login, Token
│   │   │   ├── espacio.py       # Schemas Pydantic: Espacio
│   │   │   ├── reserva.py       # Schemas Pydantic: Reserva
│   │   │   └── usuario.py       # Schemas Pydantic: Usuario
│   │   ├── services/
│   │   │   └── auth_service.py  # JWT, hashing, guards de rol
│   │   ├── db.py                # Conexión SQLAlchemy + get_db
│   │   └── main.py              # App FastAPI + creación de admin inicial
│   ├── .dockerignore
│   ├── Dockerfile
│   └── requirements.txt
├── frontend/
│   ├── css/
│   │   └── style.css
│   ├── js/
│   │   ├── api.js               # Funciones fetch reutilizables
│   │   ├── admin.js             # Lógica del panel administrador
│   │   ├── login.js             # Lógica de autenticación
│   │   └── usuario.js           # Lógica del panel usuario
│   ├── index.html               # Pantalla de selección de rol
│   ├── login.html               # Pantalla de login
│   ├── dashboard.html           # Dashboard principal post-login
│   ├── admin.html               # Panel de administrador
│   ├── usuario.html             # Panel de usuario
│   └── Dockerfile
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
| JavaScript (Vanilla) | Lógica del cliente y llamadas a la API |
| Nginx (Alpine) | Servidor web para archivos estáticos |

### Infraestructura

| Tecnología | Versión | Uso |
|---|---|---|
| Docker | — | Contenedorización |
| Docker Compose | 3.8 | Orquestación de servicios |
| PostgreSQL | 15 | Base de datos relacional |

---

## Variables de entorno

Crear un archivo `.env` en la raíz del proyecto antes de levantar los servicios:

```env
# Base de datos PostgreSQL
POSTGRES_USER=tu_usuario
POSTGRES_PASSWORD=tu_contraseña_segura
POSTGRES_DB=reservas_db

# Conexión que usa el backend
DATABASE_URL=postgresql://tu_usuario:tu_contraseña_segura@db:5432/reservas_db

# Seguridad JWT
SECRET_KEY=una-clave-secreta-muy-larga-y-segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> **Importante:** el archivo `.env` está excluido del repositorio por `.gitignore`. Nunca lo subas al control de versiones.

---

## Instalación y ejecución

### Requisitos previos

- [Docker](https://docs.docker.com/get-docker/) v20+
- [Docker Compose](https://docs.docker.com/compose/install/) v2+

### Pasos

```bash
# 1. Clonar el repositorio y cambiar a esta rama
git clone https://github.com/valentinazapata310066/ActividadFinal.git
cd ActividadFinal
git checkout main

# 2. Crear el archivo de variables de entorno
cp .env.example .env    # o crearlo manualmente con los valores indicados arriba

# 3. Construir y levantar todos los servicios
docker compose up --build

# En segundo plano:
docker compose up --build -d

# 4. Detener los servicios
docker compose down

# Eliminar también los datos de la base de datos:
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
- **Documentación automática (Swagger):** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

### Red y volúmenes

- **Red:** `reservas_network` (tipo `bridge`) — conecta los tres servicios de forma aislada.
- **Volumen:** `postgres_data` — persiste los datos de PostgreSQL entre reinicios.

---

## Arquitectura del backend

```
main.py
  └── Crea tablas (Base.metadata.create_all)
  └── Crea admin inicial si no existe
  └── Configura CORS (allow_origins=["*"])
  └── Registra routers: /auth, /usuarios, /espacios, /reservas

db.py
  └── Lee DATABASE_URL desde .env
  └── Crea engine SQLAlchemy
  └── Expone get_db() como dependencia inyectable

services/auth_service.py
  └── hashear_password / verificar_password (bcrypt)
  └── crear_token (JWT HS256)
  └── get_usuario_actual (dependencia de autenticación)
  └── get_admin_actual (dependencia de autorización admin)
```

---

## Modelos de datos

### Usuario (`tabla: usuarios`)

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
| `estado` | String | `"disponible"`, `"inactivo"`, `"mantenimiento"` |

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
| POST | `/usuarios/` | Admin | Crear usuario (con rol definido) |
| POST | `/usuarios/registro` | Público | Registro libre (rol forzado a `usuario`) |
| GET | `/usuarios/` | Admin | Listar todos los usuarios |
| GET | `/usuarios/me` | Autenticado | Ver perfil propio |
| GET | `/usuarios/{id}` | Admin | Ver usuario por ID |
| PATCH | `/usuarios/{id}` | Admin | Actualizar nombre, correo, rol, activo |

### Espacios — `/espacios`

| Método | Ruta | Acceso | Descripción |
|---|---|---|---|
| POST | `/espacios/` | Admin | Crear espacio |
| GET | `/espacios/` | Autenticado | Listar todos los espacios |
| GET | `/espacios/disponibles` | Autenticado | Listar solo espacios disponibles |
| GET | `/espacios/{id}` | Autenticado | Ver espacio por ID |
| PATCH | `/espacios/{id}` | Admin | Actualizar datos del espacio |
| DELETE | `/espacios/{id}` | Admin | Eliminar espacio |

### Reservas — `/reservas`

| Método | Ruta | Acceso | Descripción |
|---|---|---|---|
| POST | `/reservas/` | Autenticado | Crear reserva |
| GET | `/reservas/` | Autenticado | Listar reservas (admin: todas; usuario: solo las propias) |
| GET | `/reservas/mis-reservas` | Autenticado | Ver reservas del usuario actual |
| GET | `/reservas/pendientes` | Admin | Ver reservas en estado `esperando` |
| GET | `/reservas/{id}` | Autenticado | Ver reserva por ID |
| PATCH | `/reservas/{id}/estado` | Admin | Aprobar o rechazar reserva |
| DELETE | `/reservas/{id}` | Autenticado | Cancelar reserva (no se puede si está aprobada) |

---

## Lógica de negocio y validaciones

Al crear una reserva (`POST /reservas/`), el sistema aplica las siguientes validaciones en orden:

1. **Anticipación mínima:** la reserva debe realizarse con al menos **24 horas de anticipación**.
2. **Espacio existente y disponible:** el espacio debe existir y tener estado `"disponible"`.
3. **Capacidad:** `cantidad_asistentes` no puede superar la `capacidad` del espacio.
4. **Restricciones horarias:**
   - **Domingos:** no se permiten reservas.
   - **Sábados:** solo de 8:00 a 12:00.
   - **Lunes a viernes:** solo de 7:00 a 20:00.
5. **Sin superposición:** no puede haber otra reserva en el mismo espacio, misma fecha, y con rango horario solapado (estados `esperando` o `aprobada`).
6. **Validación de horas:** `hora_fin` debe ser mayor a `hora_inicio` (validado por Pydantic).

Al cancelar una reserva:
- Solo el propietario o un admin pueden cancelarla.
- No se puede cancelar una reserva con estado `"aprobada"`.

---

## Autenticación y autorización

La autenticación usa **OAuth2 con JWT Bearer tokens** (HS256).

El token contiene el payload: `{ "sub": correo, "id_usuario": int, "rol": string, "exp": timestamp }`.

Las dependencias de FastAPI `get_usuario_actual` y `get_admin_actual` protegen los endpoints automáticamente:

```python
# Cualquier usuario autenticado
usuario = Depends(get_usuario_actual)

# Solo administradores
_ = Depends(get_admin_actual)
```

Variables que configuran el JWT en `.env`:

```
SECRET_KEY=...
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

---

## Estructura del frontend

| Archivo | Descripción |
|---|---|
| `index.html` | Pantalla de bienvenida con dos botones: acceder como Admin o como Usuario. Guarda el rol en `localStorage` y redirige a `login.html`. |
| `login.html` | Formulario de login. Muestra el rol seleccionado. Al autenticarse, guarda el token en `localStorage` y redirige a `dashboard.html`. |
| `dashboard.html` | Dashboard principal con formulario de reserva y listado de espacios/reservas según el rol. |
| `admin.html` | Panel de administrador: crear espacios, listar espacios, aprobar/rechazar reservas. |
| `usuario.html` | Panel de usuario: ver espacios disponibles, crear reservas, ver y cancelar reservas propias. |
| `js/api.js` | Funciones `fetch` centralizadas: `loginUsuario`, `getEspacios`, `crearReserva`, `getReservas`, `actualizarEstadoReserva`. URL base: `http://localhost:8000`. |
| `js/login.js` | Maneja el flujo de login: decodifica el JWT para extraer el rol, guarda `token`, `rol` e `id_usuario` en `localStorage`, y redirige según el rol. |
| `js/admin.js` | Carga y muestra espacios y reservas. Funciones: `crearEspacio`, `cargarEspacios`, `aprobarReserva`, `rechazarReserva`. |
| `js/usuario.js` | Carga espacios y reservas propias. Funciones: `crearReserva`, `cargarMisReservas`, `cancelarReserva`. |
| `css/style.css` | Estilos compartidos: layout centrado, tarjetas de espacios/reservas, formularios, botones. |

---

## Flujo de uso de la aplicación

```
index.html
  ├── [Administrador] → login.html → dashboard.html / admin.html
  │     Login: admin@test.com / admin123
  │     Puede: crear espacios, ver todas las reservas, aprobar/rechazar
  │
  └── [Usuario] → login.html → dashboard.html / usuario.html
        Registro: POST /usuarios/registro
        Puede: ver espacios disponibles, crear reservas, cancelar las propias
```

---

## Usuario administrador inicial

Al iniciar la aplicación por primera vez, `main.py` crea automáticamente un usuario administrador si no existe:

| Campo | Valor |
|---|---|
| Correo | `admin@test.com` |
| Contraseña | `admin123` |
| Rol | `admin` |

> **Importante:** cambiar estas credenciales en producción.

---

## Archivos ignorados

```gitignore
desktop.ini
venv/
__pycache__/
.env
*.pyc
```