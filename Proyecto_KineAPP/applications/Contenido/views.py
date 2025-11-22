from django.shortcuts import render

# ===========================
#  VISTAS BÁSICAS DE CONTENIDO
# ===========================

from django.shortcuts import render

def temas_list(request):
    return render(request, "contenido/temas_list.html")


def tema_detalle(request, tema_id):
    return render(request, "contenido/tema_detalle.html")


def videos_del_tema(request, tema_id):
    return render(request, "contenido/videos_del_tema.html")


def preguntas_del_video(request, video_id):
    return render(request, "contenido/preguntas_del_video.html")
