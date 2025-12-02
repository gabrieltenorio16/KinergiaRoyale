from django.shortcuts import get_object_or_404, render

from .models import Video

# ===========================
#  VISTAS BASICAS DE CONTENIDO
# ===========================


def temas_list(request):
    return render(request, "contenido/temas_list.html")


def tema_detalle(request, tema_id):
    return render(request, "contenido/tema_detalle.html")


def videos_del_tema(request, tema_id):
    return render(request, "contenido/videos_del_tema.html")


def preguntas_del_video(request, video_id):
    video = get_object_or_404(
        Video.objects.prefetch_related("preguntas"),
        pk=video_id,
    )
    preguntas = video.preguntas.all()

    return render(
        request,
        "contenido/preguntas_del_video.html",
        {
            "video": video,
            "preguntas": preguntas,
        },
    )
