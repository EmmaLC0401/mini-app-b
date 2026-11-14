from fastapi.testclient import TestClient

from app.main import app

cliente = TestClient(app)


def test_listar_tareas_filtradas_por_estado():
    pendiente = cliente.post(
        "/api/tareas",
        json={"titulo": "Tarea pendiente para filtrar"},
    ).json()
    completada = cliente.post(
        "/api/tareas",
        json={"titulo": "Tarea completada para filtrar"},
    ).json()
    completada = cliente.put(
        f"/api/tareas/{completada['id']}/completar"
    ).json()

    respuesta_pendientes = cliente.get("/api/tareas?estado=pendientes")
    respuesta_completadas = cliente.get("/api/tareas?estado=completadas")

    assert respuesta_pendientes.status_code == 200
    assert pendiente in respuesta_pendientes.json()
    assert completada not in respuesta_pendientes.json()
    assert respuesta_completadas.status_code == 200
    assert completada in respuesta_completadas.json()
    assert pendiente not in respuesta_completadas.json()


def test_listar_tareas_rechaza_estado_invalido():
    respuesta = cliente.get("/api/tareas?estado=archivadas")

    assert respuesta.status_code == 422
