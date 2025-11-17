# applications/curso_y_modulo/urls.py

from django.urls import path
from . import views

urlpatterns = [
    # Cuando el usuario navegue a /simulacion/, se ejecuta la función simulacion_video
    path("simulacion/<int:pk>/",views.VideoDetailView.as_view(), name="simulacion"),
    path("simulacion/<int:pk>/crear-ficha/", views.FichaPacienteCreate.as_view(), name="crear_ficha_paciente"),
]
