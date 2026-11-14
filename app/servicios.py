from typing import Literal, TypedDict

EstadoTareas = Literal["pendientes", "completadas"]


class Tarea(TypedDict):
    id: int
    titulo: str
    completada: bool


_tareas: list[Tarea] = []
_siguiente_id = 1


def listar_tareas(estado: EstadoTareas | None = None) -> list[Tarea]:
    return [
        tarea.copy()
        for tarea in _tareas
        if estado is None
        or tarea["completada"] == (estado == "completadas")
    ]


def crear_tarea(titulo: str) -> Tarea:
    global _siguiente_id

    tarea: Tarea = {
        "id": _siguiente_id,
        "titulo": titulo,
        "completada": False,
    }
    _tareas.append(tarea)
    _siguiente_id += 1
    return tarea.copy()


def completar_tarea(id_tarea: int) -> Tarea | None:
    for tarea in _tareas:
        if tarea["id"] == id_tarea:
            tarea["completada"] = True
            return tarea.copy()
    return None


def eliminar_tarea(id_tarea: int) -> bool:
    for indice, tarea in enumerate(_tareas):
        if tarea["id"] == id_tarea:
            del _tareas[indice]
            return True
    return False
