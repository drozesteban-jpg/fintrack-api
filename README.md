# FinTrack API

![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat&logo=fastapi&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-15-336791?style=flat&logo=postgresql&logoColor=white)
![SQLAlchemy](https://img.shields.io/badge/SQLAlchemy-2.0-D71F00?style=flat)
![Alembic](https://img.shields.io/badge/Alembic-1.18-6BA539?style=flat)
![pytest](https://img.shields.io/badge/pytest-9.0-0A9EDC?style=flat&logo=pytest&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

API REST para seguimiento de finanzas personales. Permite registrar ingresos y gastos, consultarlos por categoría y obtener un resumen del balance.

---

## Funcionalidades

- Registro y login de usuarios con JWT
- Registrar ingresos y gastos con categoría y descripción
- Listar todas las transacciones (con filtros y paginación)
- Consultar una transacción por ID
- Eliminar transacciones
- Obtener resumen financiero con balance total

---

## Tecnologías

- **Python 3.14**
- **FastAPI** — framework web
- **PostgreSQL** — base de datos
- **SQLAlchemy 2.0** — ORM
- **Alembic** — migraciones de base de datos
- **Pydantic** — validación de datos
- **python-jose** — generación y verificación de JWT
- **passlib + bcrypt** — hash de contraseñas
- **pytest + httpx** — tests unitarios

---

## Instalación

```bash
git clone https://github.com/drozesteban-jpg/fintrack-api.git
cd fintrack-api
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Creá un archivo `.env` en la raíz con este contenido:

```env
DATABASE_URL=postgresql://usuario:contraseña@localhost:5432/fintrack
SECRET_KEY=tu_clave_secreta
```

Ejecutá las migraciones:

```bash
alembic upgrade head
```

---

## Uso

Iniciá el servidor:

```bash
uvicorn main:app --reload
```

Accedé a la documentación interactiva en:

```
http://127.0.0.1:8000/docs
```

---

## Autenticación

Todos los endpoints de transacciones requieren autenticación mediante JWT. El flujo es:

1. Registrarse en `POST /auth/registro`
2. Obtener un token en `POST /auth/login`
3. Incluir el token en cada request: `Authorization: Bearer <token>`

---

## Endpoints

### Autenticación

| Método | Ruta | Descripción | Auth |
|--------|------|-------------|------|
| POST | /auth/registro | Registrar nuevo usuario | No |
| POST | /auth/login | Obtener token JWT | No |

### Transacciones

Todos los endpoints filtran automáticamente por el usuario autenticado.

| Método | Ruta | Descripción | Auth |
|--------|------|-------------|------|
| POST | /transacciones | Crear una transacción | Sí |
| GET | /transacciones | Listar transacciones (con filtros) | Sí |
| GET | /transacciones/{id} | Obtener transacción por ID | Sí |
| DELETE | /transacciones/{id} | Eliminar una transacción | Sí |
| GET | /resumen | Ver balance total | Sí |

**Parámetros de filtro para `GET /transacciones`:**

| Parámetro | Tipo | Descripción |
|-----------|------|-------------|
| `skip` | int | Offset para paginación (default: 0) |
| `limit` | int | Máximo de resultados (default: 20, máx: 100) |
| `tipo` | str | Filtrar por `ingreso` o `gasto` |
| `categoria` | str | Filtrar por categoría (texto exacto) |

---

## Ejemplo de uso

**1. Registrar usuario:**

```bash
curl -X POST http://127.0.0.1:8000/auth/registro \
  -H "Content-Type: application/json" \
  -d '{"email": "usuario@ejemplo.com", "password": "mi_clave"}'
```

Respuesta:

```json
{
  "id": 1,
  "email": "usuario@ejemplo.com"
}
```

**2. Iniciar sesión:**

```bash
curl -X POST http://127.0.0.1:8000/auth/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=usuario@ejemplo.com&password=mi_clave"
```

Respuesta:

```json
{
  "access_token": "eyJ...",
  "token_type": "bearer"
}
```

**3. Crear una transacción:**

```bash
curl -X POST http://127.0.0.1:8000/transacciones \
  -H "Authorization: Bearer eyJ..." \
  -H "Content-Type: application/json" \
  -d '{"descripcion": "Supermercado", "monto": 5000, "tipo": "gasto", "categoria": "alimentacion"}'
```

Respuesta:

```json
{
  "id": 1,
  "descripcion": "Supermercado",
  "monto": 5000,
  "tipo": "gasto",
  "categoria": "alimentacion",
  "fecha": "2026-04-12T20:33:19"
}
```

---

## Tests

El proyecto incluye tests unitarios completos con pytest. Cubren autenticación, CRUD de transacciones, filtros, paginación, resumen y aislamiento entre usuarios.

```bash
pytest tests/
```

---

## Estructura del proyecto

```
fintrack-api/
├── main.py
├── requirements.txt
├── .env
├── .gitignore
├── README.md
├── alembic.ini
├── alembic/
│   └── versions/
├── app/
│   ├── __init__.py
│   ├── database.py
│   ├── models.py
│   ├── schemas.py
│   └── routers.py
└── tests/
    ├── __init__.py
    ├── conftest.py
    └── test_main.py
```

---

## Autor

**Esteban Droz** — [@drozesteban-jpg](https://github.com/drozesteban-jpg)

Proyecto desarrollado para consolidar conocimientos en Python backend, APIs REST y bases de datos relacionales.