def test_crear_transaccion(client):
    respuesta = client.post("/transacciones", json={
        "descripcion": "Supermercado",
        "monto": 5000,
        "tipo": "gasto",
        "categoria": "alimentacion"
    })
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert datos["descripcion"] == "Supermercado"
    assert datos["monto"] == 5000
    assert datos["tipo"] == "gasto"


def test_listar_transacciones(client):
    respuesta = client.get("/transacciones")
    assert respuesta.status_code == 200
    assert isinstance(respuesta.json(), list)


def _crear(client, tipo, categoria, monto=1000):
    client.post("/transacciones", json={
        "descripcion": "test", "monto": monto, "tipo": tipo, "categoria": categoria
    })


def test_paginacion(client):
    for _ in range(5):
        _crear(client, "gasto", "ocio")
    respuesta = client.get("/transacciones?skip=0&limit=3")
    assert respuesta.status_code == 200
    assert len(respuesta.json()) <= 3


def test_filtro_por_tipo(client):
    _crear(client, "ingreso", "salario")
    _crear(client, "gasto", "transporte")
    respuesta = client.get("/transacciones?tipo=ingreso")
    assert respuesta.status_code == 200
    assert all(t["tipo"] == "ingreso" for t in respuesta.json())


def test_filtro_por_categoria(client):
    _crear(client, "gasto", "salud")
    _crear(client, "gasto", "ocio")
    respuesta = client.get("/transacciones?categoria=salud")
    assert respuesta.status_code == 200
    assert all(t["categoria"] == "salud" for t in respuesta.json())


def test_filtro_tipo_invalido(client):
    respuesta = client.get("/transacciones?tipo=invalido")
    assert respuesta.status_code == 422


def test_skip_negativo(client):
    respuesta = client.get("/transacciones?skip=-1")
    assert respuesta.status_code == 422


def test_crear_transaccion_monto_invalido(client):
    respuesta = client.post("/transacciones", json={
        "descripcion": "Error",
        "monto": -100,
        "tipo": "gasto",
        "categoria": "test"
    })
    assert respuesta.status_code == 422


def test_crear_transaccion_tipo_invalido(client):
    respuesta = client.post("/transacciones", json={
        "descripcion": "Error",
        "monto": 1000,
        "tipo": "invalido",
        "categoria": "test"
    })
    assert respuesta.status_code == 422


def test_resumen(client):
    respuesta = client.get("/resumen")
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert "ingresos_totales" in datos
    assert "gastos_totales" in datos
    assert "balance" in datos
