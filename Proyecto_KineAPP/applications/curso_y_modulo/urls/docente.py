# applications/curso_y_modulo/urls/docente.py

from django.urls import path
from applications.curso_y_modulo.views.docente import (
    panel_maestro_docente,
    panel_maestro_estudiantes,
    panel_maestro_recursos,
    docente_dashboard,
    crear_curso_view,
    editar_curso_view,
    agregar_estudiantes_view,
    curso_estudiantes,
)
from applications.curso_y_modulo.views.contenido import asignar_contenido, asignar_pacientes

app_name = "docente"

urlpatterns = [
    path("panel/", panel_maestro_docente, name="panel"),
    path("dashboard/", docente_dashboard, name="docente_dashboard"),
    path("estudiantes/", panel_maestro_estudiantes, name="estudiantes"),
    path("recursos/", panel_maestro_recursos, name="recursos"),
    path("curso/crear/", crear_curso_view, name="crear_curso"),
    path("curso/<int:curso_id>/editar/", editar_curso_view, name="editar_curso"),
    path("curso/<int:curso_id>/agregar-estudiantes/", agregar_estudiantes_view,
         name="agregar_estudiantes"),
    path("curso/<int:curso_id>/estudiantes/", curso_estudiantes, name="curso_estudiantes"),
    path("curso/<int:curso_id>/asignar/", asignar_contenido, name="asignar_contenido"),
    path("curso/<int:curso_id>/pacientes/", asignar_pacientes, name="asignar_pacientes"),
]
