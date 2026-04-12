# FinTrack API

![Python](https://img.shields.io/badge/Python-3.14-3776AB?style=flat&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688?style=flat&logo=fastapi&logoColor=white)
![SQLite](https://img.shields.io/badge/SQLite-3-003B57?style=flat&logo=sqlite&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

API REST para seguimiento de finanzas personales. Permite registrar ingresos y gastos, consultarlos por categoría y obtener un resumen del balance mensual.

---

## Funcionalidades

- Registrar ingresos y gastos con categoría y descripción
- Listar todas las transacciones
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

## Endpoints

| Método | Ruta | Descripción |
|--------|------|-------------|
| POST | /transacciones | Crear una transacción |
| GET | /transacciones | Listar todas las transacciones |
| GET | /transacciones/{id} | Obtener transacción por ID |
| DELETE | /transacciones/{id} | Eliminar una transacción |
| GET | /resumen | Ver balance total |

---

## Ejemplo de uso

Crear un gasto:

```json
{
  "descripcion": "Supermercado",
  "monto": 5000,
  "tipo": "gasto",
  "categoria": "alimentacion"
}
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