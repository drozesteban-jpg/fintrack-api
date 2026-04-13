def test_registro(client):
    resp = client.post("/auth/registro", json={"email": "u@test.com", "password": "pass123"})
    assert resp.status_code == 201
    assert resp.json()["email"] == "u@test.com"


def test_registro_email_duplicado(client):
    client.post("/auth/registro", json={"email": "dup@test.com", "password": "pass"})
    resp = client.post("/auth/registro", json={"email": "dup@test.com", "password": "pass"})
    assert resp.status_code == 400


def test_login(client):
    client.post("/auth/registro", json={"email": "u@test.com", "password": "pass123"})
    resp = client.post("/auth/login", data={"username": "u@test.com", "password": "pass123"})
    assert resp.status_code == 200
    assert "access_token" in resp.json()


def test_login_credenciales_invalidas(client):
    resp = client.post("/auth/login", data={"username": "no@existe.com", "password": "wrong"})
    assert resp.status_code == 401


def test_endpoint_sin_token(client):
    resp = client.get("/transacciones")
    assert resp.status_code == 401


def test_crear_transaccion(client, auth_headers):
    respuesta = client.post("/transacciones", json={
        "descripcion": "Supermercado",
        "monto": 5000,
        "tipo": "gasto",
        "categoria": "alimentacion"
    }, headers=auth_headers)
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert datos["descripcion"] == "Supermercado"
    assert datos["monto"] == 5000
    assert datos["tipo"] == "gasto"


def test_listar_transacciones(client, auth_headers):
    respuesta = client.get("/transacciones", headers=auth_headers)
    assert respuesta.status_code == 200
    assert isinstance(respuesta.json(), list)


def _crear(client, headers, tipo, categoria, monto=1000):
    client.post("/transacciones", json={
        "descripcion": "test", "monto": monto, "tipo": tipo, "categoria": categoria
    }, headers=headers)


def test_paginacion(client, auth_headers):
    for _ in range(5):
        _crear(client, auth_headers, "gasto", "ocio")
    respuesta = client.get("/transacciones?skip=0&limit=3", headers=auth_headers)
    assert respuesta.status_code == 200
    assert len(respuesta.json()) <= 3


def test_filtro_por_tipo(client, auth_headers):
    _crear(client, auth_headers, "ingreso", "salario")
    _crear(client, auth_headers, "gasto", "transporte")
    respuesta = client.get("/transacciones?tipo=ingreso", headers=auth_headers)
    assert respuesta.status_code == 200
    assert all(t["tipo"] == "ingreso" for t in respuesta.json())


def test_filtro_por_categoria(client, auth_headers):
    _crear(client, auth_headers, "gasto", "salud")
    _crear(client, auth_headers, "gasto", "ocio")
    respuesta = client.get("/transacciones?categoria=salud", headers=auth_headers)
    assert respuesta.status_code == 200
    assert all(t["categoria"] == "salud" for t in respuesta.json())


def test_filtro_tipo_invalido(client, auth_headers):
    respuesta = client.get("/transacciones?tipo=invalido", headers=auth_headers)
    assert respuesta.status_code == 422


def test_skip_negativo(client, auth_headers):
    respuesta = client.get("/transacciones?skip=-1", headers=auth_headers)
    assert respuesta.status_code == 422


def test_crear_transaccion_monto_invalido(client, auth_headers):
    respuesta = client.post("/transacciones", json={
        "descripcion": "Error",
        "monto": -100,
        "tipo": "gasto",
        "categoria": "test"
    }, headers=auth_headers)
    assert respuesta.status_code == 422


def test_crear_transaccion_tipo_invalido(client, auth_headers):
    respuesta = client.post("/transacciones", json={
        "descripcion": "Error",
        "monto": 1000,
        "tipo": "invalido",
        "categoria": "test"
    }, headers=auth_headers)
    assert respuesta.status_code == 422


def test_resumen(client, auth_headers):
    respuesta = client.get("/resumen", headers=auth_headers)
    assert respuesta.status_code == 200
    datos = respuesta.json()
    assert "ingresos_totales" in datos
    assert "gastos_totales" in datos
    assert "balance" in datos


def test_aislamiento_entre_usuarios(client):
    """Cada usuario solo ve sus propias transacciones."""
    # Usuario A
    client.post("/auth/registro", json={"email": "a@test.com", "password": "pass"})
    resp_a = client.post("/auth/login", data={"username": "a@test.com", "password": "pass"})
    headers_a = {"Authorization": f"Bearer {resp_a.json()['access_token']}"}

    # Usuario B
    client.post("/auth/registro", json={"email": "b@test.com", "password": "pass"})
    resp_b = client.post("/auth/login", data={"username": "b@test.com", "password": "pass"})
    headers_b = {"Authorization": f"Bearer {resp_b.json()['access_token']}"}

    _crear(client, headers_a, "ingreso", "salario")

    assert len(client.get("/transacciones", headers=headers_a).json()) == 1
    assert len(client.get("/transacciones", headers=headers_b).json()) == 0
