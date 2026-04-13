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
