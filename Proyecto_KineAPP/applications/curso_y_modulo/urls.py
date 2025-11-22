# applications/curso_y_modulo/urls.py

from django.urls import path
from . import views

app_name = "curso_y_modulo"

urlpatterns = [
    # Simulación de video
    path("simulacion/<int:pk>/", views.VideoDetailView.as_view(), name="simulacion"),
    path("simulacion/<int:pk>/crear-ficha/", views.FichaPacienteCreate.as_view(), name="crear_ficha_paciente"),

    # NUEVAS RUTAS PARA LA PANTALLA DEL CURSO
    path("curso/<int:curso_id>/", views.curso_detalle, name="curso_detalle"),
    path(
        "curso/<int:curso_id>/seleccionar-paciente/<int:paciente_id>/",
        views.seleccionar_paciente_curso,
        name="seleccionar_paciente_curso",
    ),
]
