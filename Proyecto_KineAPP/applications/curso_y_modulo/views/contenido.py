# applications/curso_y_modulo/views/contenido.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Prefetch

from applications.curso_y_modulo.models import Curso, ContenidoAsignado
from applications.Contenido.models import Tema, Video


@login_required
def asignar_contenido(request, curso_id):

    if request.user.rol != "DOC":
        messages.error(request, "No tienes permisos para acceder a esta sección.")
        return redirect("root_redirect")

    curso = get_object_or_404(Curso, pk=curso_id)

    temas = Tema.objects.filter(curso=curso).prefetch_related(
        Prefetch("video_set", queryset=Video.objects.all())
    )

    if request.method == "POST":
        videos_seleccionados = request.POST.getlist("videos_seleccionados")

        for estudiante in curso.estudiantes.all():
            for video_id in videos_seleccionados:
                ContenidoAsignado.objects.get_or_create(
                    curso=curso,
                    video_id=video_id,
                    estudiante=estudiante
                )

        messages.success(request, "Contenido asignado con éxito.")
        return redirect("docente:asignar_contenido", curso_id=curso.id)

    return render(request, "docente/asignar_contenido.html", {
        "curso": curso,
        "temas": temas,
    })
