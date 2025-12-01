from django.urls import path

# Importar vistas desde los nuevos módulos separados
from applications.curso_y_modulo.views.estudiante import (
    curso_detalle,
    seleccionar_paciente_curso,
)

from applications.curso_y_modulo.views.contenido import (
    asignar_contenido
)

app_name = "curso"

urlpatterns = [
    path("<int:curso_id>/", curso_detalle, name="curso_detalle"),

    path("<int:curso_id>/seleccionar-paciente/<int:paciente_id>/",
         seleccionar_paciente_curso,
         name="seleccionar_paciente_curso"),

    path("<int:curso_id>/asignar-contenido/",
         asignar_contenido,
         name="asignar_contenido"),
]
