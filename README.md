# FinTrack API

![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat&logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=flat&logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

API REST para seguimiento de finanzas personales. Permite registrar ingresos y gastos, consultarlos por categoría y obtener un resumen del balance mensual.

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

- Python 3.14
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Uvicorn
- python-jose (JWT)
- passlib (bcrypt)

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
DATABASE_URL=sqlite:///./fintrack.db
SECRET_KEY=mi_clave_secreta
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
3. Incluir el token en cada request como header: `Authorization: Bearer <token>`

---

## Endpoints

### Autenticación

| Método | Ruta | Descripción | Auth |
|--------|------|-------------|------|
| POST | /auth/registro | Registrar nuevo usuario | No |
| POST | /auth/login | Obtener token JWT | No |

### Transacciones

Todos los endpoints de transacciones filtran automáticamente por el usuario autenticado.

| Método | Ruta | Descripción | Auth |
|--------|------|-------------|------|
| POST | /transacciones | Crear una transacción | Si |
| GET | /transacciones | Listar transacciones (con filtros) | Si |
| GET | /transacciones/{id} | Obtener transacción por ID | Si |
| DELETE | /transacciones/{id} | Eliminar una transacción | Si |
| GET | /resumen | Ver balance total | Si |

**Parámetros de filtro para `GET /transacciones`:**
- `skip` — offset para paginación (default: 0)
- `limit` — máximo de resultados (default: 20, máx: 100)
- `tipo` — filtrar por `ingreso` o `gasto`
- `categoria` — filtrar por categoría (texto exacto)

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

## Estructura del proyecto

```
fintrack-api/
├── main.py
├── requirements.txt
├── .env
├── .gitignore
├── README.md
└── app/
    ├── __init__.py
    ├── database.py
    ├── models.py
    ├── schemas.py
    └── routers.py
```

---

## Autor

**Esteban Droz** — [@drozesteban-jpg](https://github.com/drozesteban-jpg)

Proyecto desarrollado para consolidar conocimientos en Python backend, APIs REST y bases de datos relacionales.