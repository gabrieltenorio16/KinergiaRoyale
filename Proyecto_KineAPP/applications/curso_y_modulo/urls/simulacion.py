# applications/curso_y_modulo/urls/simulacion.py

from django.urls import path
from applications.curso_y_modulo.views.simulacion import (
    VideoDetailView,
    FichaPacienteCreate,
)

app_name = "simulacion"

urlpatterns = [
    path("<int:pk>/", VideoDetailView.as_view(), name="simulacion"),
    path("<int:pk>/crear-paciente/", FichaPacienteCreate.as_view(), name="crear_paciente"),
]
