from django.urls import path

# Importar vistas desde los módulos separados
from applications.curso_y_modulo.views.docente import (
    panel_maestro_docente,
    panel_maestro_estudiantes,
    panel_maestro_recursos,
    crear_curso_view,
    agregar_estudiantes_view,
)

from applications.curso_y_modulo.views.contenido import (
    asignar_contenido
)

app_name = "docente"

urlpatterns = [
    path("panel/", panel_maestro_docente, name="panel"),
    path("estudiantes/", panel_maestro_estudiantes, name="estudiantes"),
    path("recursos/", panel_maestro_recursos, name="recursos"),

    # Acciones
    path("curso/crear/", crear_curso_view, name="crear_curso"),
    path("curso/<int:curso_id>/agregar-estudiantes/", agregar_estudiantes_view, name="agregar_estudiantes"),

    # Asignación contenido
    path("curso/<int:curso_id>/asignar/", asignar_contenido, name="asignar_contenido"),

]
