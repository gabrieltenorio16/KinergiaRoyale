# applications/curso_y_modulo/urls/curso.py

from django.urls import path

# Vistas de estudiante
from applications.curso_y_modulo.views.estudiante import (
    curso_detalle,
    seleccionar_paciente_curso,
)

# Vistas de contenido (para asignar contenido al curso)
from applications.curso_y_modulo.views.contenido import (
    asignar_contenido,
)

# 👇 IMPORTANTE para poder usar namespace="curso"
app_name = "curso"

urlpatterns = [
    # Detalle del curso (panel interno del estudiante para un curso)
    # URL final: /curso/<curso_id>/
    path(
        "<int:curso_id>/",
        curso_detalle,
        name="curso_detalle",
    ),

    # Seleccionar paciente dentro del curso
    # URL final: /curso/<curso_id>/seleccionar-paciente/<paciente_id>/
    path(
        "<int:curso_id>/seleccionar-paciente/<int:paciente_id>/",
        seleccionar_paciente_curso,
        name="seleccionar_paciente_curso",
    ),

    # Asignar contenido a un curso (puede ser usado por vistas de docente)
    # URL final: /curso/<curso_id>/asignar-contenido/
    path(
        "<int:curso_id>/asignar-contenido/",
        asignar_contenido,
        name="asignar_contenido",
    ),
]
