# applications/Contenido/urls.py

from django.urls import path
from . import views

app_name = "Contenido"

urlpatterns = [
    # Lista de temas
    path("temas/", views.temas_list, name="temas_list"),

    # Detalle de un tema específico
    path("tema/<int:tema_id>/", views.tema_detalle, name="tema_detalle"),

    # Videos de un tema
    path("tema/<int:tema_id>/videos/", views.videos_del_tema, name="videos_del_tema"),

    path("video/curso/<int:video_id>/", views.preguntas_del_video, name="preguntas_del_video")

]
