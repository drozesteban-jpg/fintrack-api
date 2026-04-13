# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Commands

**Setup:**
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Requires a `.env` file at the project root:
```
DATABASE_URL=sqlite:///./fintrack.db
SECRET_KEY=mi_clave_secreta
```

**Run the server:**
```bash
uvicorn main:app --reload
```

**Run tests:**
```bash
pytest
pytest tests/test_main.py::test_crear_transaccion  # single test
```

Interactive API docs available at `http://127.0.0.1:8000/docs`.

## Architecture

This is a FastAPI + SQLAlchemy + SQLite REST API with no authentication layer.

**Request flow:** `main.py` → `app/routers.py` → `app/models.py` (SQLAlchemy ORM) via a `Session` dependency injected from `app/database.py`.

**Key design decisions:**
- `app/schemas.py` defines two Pydantic model layers: `TransaccionCreate` (input with validators) and `TransaccionResponse` (output with `from_attributes=True` for ORM serialization). Validation of `tipo` ("ingreso"/"gasto") and positive `monto` happens here via `@field_validator`.
- The DB session (`get_db`) is a generator-based dependency yielded per request and closed in `finally`.
- `Base.metadata.create_all(bind=engine)` in `main.py` creates the SQLite schema on startup — there are no Alembic migrations in use despite Alembic being in `requirements.txt`.
- Tests use FastAPI's `TestClient` against the real SQLite database (not mocked), so test runs mutate `fintrack.db`.
