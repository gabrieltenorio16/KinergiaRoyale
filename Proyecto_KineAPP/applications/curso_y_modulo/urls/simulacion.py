# applications/curso_y_modulo/urls/simulacion.py

from django.urls import path
from applications.curso_y_modulo.views.simulacion import (
    VideoDetailView,
    guardar_ficha_clinica_estudiante,
)

app_name = "simulacion"

urlpatterns = [
    path("<int:pk>/", VideoDetailView.as_view(), name="simulacion"),
    path("<int:pk>/ficha-clinica/", guardar_ficha_clinica_estudiante, name="guardar_ficha_clinica"),
]

