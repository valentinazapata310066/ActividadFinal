# ActividadFinal — Rama `dev`

> **Sistema de Reservas de Espacios Institucionales**  
> Rama de desarrollo — código funcional idéntico a `main`, sin archivos de contenedorización Docker.

[![Python](https://img.shields.io/badge/Python-3.12-blue)](https://www.python.org/) [![FastAPI](https://img.shields.io/badge/FastAPI-0.136.3-green)](https://fastapi.tiangolo.com/) [![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-blue)](https://www.postgresql.org/)

---

## Descripción general

Esta rama contiene exactamente el mismo código fuente de la aplicación que la rama `main` (backend FastAPI + frontend HTML/JS/CSS), pero **no incluye los archivos de Docker** (`Dockerfile` del backend, `Dockerfile` del frontend, ni `docker-compose.yml`). Está orientada al desarrollo local directo, sin orquestación de contenedores.

---

## Diferencias respecto a `main`

| Archivo | `main` | `dev` |
|---|---|---|
| `backend/Dockerfile` | ✅ Presente | ❌ Ausente |
| `backend/.dockerignore` | ✅ Presente | ❌ Ausente |
| `frontend/Dockerfile` | ✅ Presente | ❌ Ausente |
| `docker-compose.yml` | ✅ Presente | ❌ Ausente |
| Código fuente | Idéntico | Idéntico |

> Para ejecutar en contenedores, usar la rama `main` o `ops`.

---

## Tabla de contenidos

- [Estructura del repositorio](#estructura-del-repositorio)
- [Tecnologías y dependencias](#tecnologías-y-dependencias)
- [Variables de entorno](#variables-de-entorno)
- [Ejecución local del backend](#ejecución-local-del-backend)
- [Ejecución local del frontend](#ejecución-local-del-frontend)
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
ActividadFinal-dev/
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
│   └── usuario.html             # Panel de usuario
└── .gitignore
```

> **Nota:** no hay `Dockerfile` ni `docker-compose.yml` en esta rama.

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

---

## Variables de entorno

Crear un archivo `.env` en la raíz del proyecto:

```env
# Base de datos PostgreSQL (instancia local o remota)
DATABASE_URL=postgresql://tu_usuario:tu_contraseña@localhost:5432/reservas_db

# Seguridad JWT
SECRET_KEY=una-clave-secreta-muy-larga-y-segura
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

> En esta rama no hay `docker-compose.yml`, por lo que `DATABASE_URL` debe apuntar a una instancia de PostgreSQL que esté corriendo en tu máquina local o en un servidor accesible.

---

## Ejecución local del backend

### Requisitos previos

- Python 3.12+
- PostgreSQL corriendo localmente (o accesible por red)

### Pasos

```bash
# 1. Clonar y cambiar a la rama dev
git clone https://github.com/valentinazapata310066/ActividadFinal.git
cd ActividadFinal
git checkout dev

# 2. Crear entorno virtual
cd backend
python -m venv venv
source venv/bin/activate        # Linux / macOS
venv\Scripts\activate           # Windows

# 3. Instalar dependencias
pip install -r requirements.txt

# 4. Crear el archivo .env en la raíz del proyecto con las variables indicadas arriba

# 5. Ejecutar el servidor de desarrollo
uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
```

El backend estará disponible en:
- API: http://localhost:8000
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

Al iniciar, se crean automáticamente las tablas en la base de datos y el usuario administrador inicial.

---

## Ejecución local del frontend

Como los archivos del frontend son HTML/CSS/JS estáticos, se puede servir con cualquier servidor local:

**Opción 1 — Python:**
```bash
cd frontend
python -m http.server 3000
# Abrir http://localhost:3000
```

**Opción 2 — Node.js:**
```bash
cd frontend
npx serve .
```

**Opción 3 — Extensión Live Server de VS Code:**
Abrir `frontend/index.html` con Live Server.

> La URL base del backend en el frontend está configurada como `http://localhost:8000` en `js/api.js`.

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
| POST | `/usuarios/` | Admin | Crear usuario |
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
| GET | `/reservas/` | Autenticado | Listar reservas (admin: todas; usuario: propias) |
| GET | `/reservas/mis-reservas` | Autenticado | Ver reservas del usuario actual |
| GET | `/reservas/pendientes` | Admin | Ver reservas en estado `esperando` |
| GET | `/reservas/{id}` | Autenticado | Ver reserva por ID |
| PATCH | `/reservas/{id}/estado` | Admin | Aprobar o rechazar reserva |
| DELETE | `/reservas/{id}` | Autenticado | Cancelar reserva |

---

## Lógica de negocio y validaciones

Al crear una reserva (`POST /reservas/`), el sistema valida:

1. **Anticipación mínima:** la reserva debe hacerse con al menos **24 horas de anticipación**.
2. **Espacio existente y disponible:** estado debe ser `"disponible"`.
3. **Capacidad:** `cantidad_asistentes` ≤ capacidad del espacio.
4. **Restricciones horarias:**
   - **Domingos:** no se permiten reservas.
   - **Sábados:** solo de 8:00 a 12:00.
   - **Lunes a viernes:** solo de 7:00 a 20:00.
5. **Sin superposición de horarios:** no puede existir otra reserva en el mismo espacio y fecha con rango solapado (estados `esperando` o `aprobada`).
6. **Validación de horas:** `hora_fin` > `hora_inicio` (Pydantic).

Al cancelar:
- Solo el propietario o un admin pueden cancelar.
- No se puede cancelar si el estado es `"aprobada"`.

---

## Autenticación y autorización

Usa **OAuth2 con JWT Bearer tokens** (algoritmo HS256).

Payload del token: `{ "sub": correo, "id_usuario": int, "rol": string, "exp": timestamp }`.

Dependencias de FastAPI que protegen los endpoints:

```python
get_usuario_actual   # Requiere cualquier usuario autenticado
get_admin_actual     # Requiere rol "admin"
```

---

## Estructura del frontend

| Archivo | Descripción |
|---|---|
| `index.html` | Pantalla de bienvenida. Dos botones: acceder como Admin o como Usuario. Guarda el rol en `localStorage` y redirige a `login.html`. |
| `login.html` | Formulario de login. Muestra el rol seleccionado. Guarda el token y redirige a `dashboard.html`. |
| `dashboard.html` | Dashboard con formulario de reserva, listado de espacios y reservas según el rol del usuario. |
| `admin.html` | Panel del administrador: crear espacios, listar espacios, aprobar/rechazar reservas. |
| `usuario.html` | Panel del usuario: ver espacios, crear reservas, ver y cancelar reservas propias. |
| `js/api.js` | Funciones `fetch` centralizadas. URL base: `http://localhost:8000`. |
| `js/login.js` | Maneja login, decodifica JWT, guarda `token`/`rol`/`id_usuario` en `localStorage` y redirige. |
| `js/admin.js` | Lógica del panel admin: `crearEspacio`, `cargarEspacios`, `aprobarReserva`, `rechazarReserva`. |
| `js/usuario.js` | Lógica del panel usuario: `crearReserva`, `cargarMisReservas`, `cancelarReserva`. |
| `css/style.css` | Estilos compartidos: layout, tarjetas, formularios, botones. |

---

## Flujo de uso de la aplicación

```
index.html
  ├── [Administrador] → login.html → dashboard.html / admin.html
  │     Credenciales: admin@test.com / admin123
  │     Puede: crear espacios, ver todas las reservas, aprobar/rechazar
  │
  └── [Usuario] → login.html → dashboard.html / usuario.html
        Registro: POST /usuarios/registro
        Puede: ver espacios disponibles, crear reservas, cancelar las propias
```

---

## Usuario administrador inicial

Al iniciar el backend por primera vez, `main.py` crea automáticamente:

| Campo | Valor |
|---|---|
| Correo | `admin@test.com` |
| Contraseña | `admin123` |
| Rol | `admin` |

> **Importante:** cambiar estas credenciales antes de usar en producción.

---

## Archivos ignorados

```gitignore
desktop.ini
venv/
__pycache__/
.env
*.pyc
```