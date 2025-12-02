# applications/Contenido/views.py
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect

from .models import Video


def temas_list(request):
    return HttpResponse("Listado de temas (pendiente de plantilla)")


def tema_detalle(request, tema_id):
    return HttpResponse(f"Detalle del tema {tema_id} (pendiente de plantilla)")


def videos_del_tema(request, tema_id):
    return HttpResponse(f"Videos del tema {tema_id} (pendiente de plantilla)")


def preguntas_del_video(request, video_id):
    """
    Vista legacy: mantiene la URL /contenido/video/<id>/preguntas/
    pero redirige a la simulación del video.
    """
    video = get_object_or_404(Video, pk=video_id)
    return redirect("simulacion:simulacion", pk=video.pk)
