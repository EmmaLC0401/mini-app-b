from pathlib import Path

from fastapi import FastAPI, HTTPException, Request, Response, status
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel, Field

from app import servicios

app = FastAPI()
templates = Jinja2Templates(directory=Path(__file__).parent / "templates")


class CrearTarea(BaseModel):
    titulo: str = Field(min_length=1, max_length=100)


@app.get("/", response_class=HTMLResponse)
def pagina_principal(request: Request) -> HTMLResponse:
    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={"tareas": servicios.listar_tareas()},
    )


@app.post("/api/tareas", status_code=status.HTTP_201_CREATED)
def crear_tarea(datos: CrearTarea) -> servicios.Tarea:
    return servicios.crear_tarea(datos.titulo)


@app.get("/api/tareas")
def listar_tareas() -> list[servicios.Tarea]:
    return servicios.listar_tareas()


@app.put("/api/tareas/{id_tarea}/completar")
def completar_tarea(id_tarea: int) -> servicios.Tarea:
    tarea = servicios.completar_tarea(id_tarea)
    if tarea is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La tarea no existe",
        )
    return tarea


@app.delete(
    "/api/tareas/{id_tarea}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
def eliminar_tarea(id_tarea: int) -> Response:
    if not servicios.eliminar_tarea(id_tarea):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="La tarea no existe",
        )
    return Response(status_code=status.HTTP_204_NO_CONTENT)
