# applications/curso_y_modulo/views/estudiante.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Prefetch
from django.urls import reverse

from applications.Contenido.models import Video, Tema
from applications.diagnostico_paciente.models import Paciente, Etapa
from applications.curso_y_modulo.models import Curso, SeleccionPacienteCurso


# =====================================================
# CURSO DETALLE (ESTUDIANTE)
# =====================================================

def curso_detalle(request, curso_id):

    if not request.user.is_authenticated:
        return redirect("usuario:login_estudiantes")

    curso = get_object_or_404(Curso, pk=curso_id)

    # pestaña activa del menú (presentacion / indice / sala / material)
    active_section = request.GET.get("section", "presentacion")

    temas = (
        Tema.objects.filter(curso=curso)
        .prefetch_related(
            Prefetch('video_set', queryset=Video.objects.prefetch_related('preguntas'))
        )
        .order_by('titulo')
    )

    pacientes = (
        Paciente.objects.filter(casos_clinicos__curso=curso)
        .distinct()
        .order_by('apellidos', 'nombres')
    )

    seleccion = (
        SeleccionPacienteCurso.objects
        .filter(usuario=request.user, curso=curso)
        .select_related('paciente')
        .first()
    )

    etapas = (
        Etapa.objects.filter(caso__curso=curso)
        .select_related('caso', 'parte_cuerpo')
        .order_by('caso', 'id')  # campo orden ya no existe en Etapa
    )

    context = {
        "curso": curso,
        "temas": temas,
        "pacientes": pacientes,
        "seleccion": seleccion,
        "etapas": etapas,
        "active_section": active_section,
    }
    return render(request, "curso/curso_detalle.html", context)


# =====================================================
# SELECCIONAR PACIENTE
# =====================================================

def seleccionar_paciente_curso(request, curso_id, paciente_id):

    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión para seleccionar un paciente.")
        return redirect("usuario:login_estudiantes")

    curso = get_object_or_404(Curso, pk=curso_id)

    paciente = (
        Paciente.objects.filter(pk=paciente_id, casos_clinicos__curso=curso)
        .distinct()
        .first()
    )
    if not paciente:
        messages.error(request, "Paciente no encontrado para este curso.")
        return redirect("curso:curso_detalle", curso_id=curso.id)

    # Guardar / actualizar selección
    SeleccionPacienteCurso.objects.update_or_create(
        usuario=request.user,
        curso=curso,
        defaults={"paciente": paciente},
    )

    # 1) Buscar una ENTREVISTA (Etapa) para este paciente en este curso
    etapa = (
        Etapa.objects.filter(
            paciente=paciente,
            caso__curso=curso,
            video__isnull=False,
        )
        .select_related("video")
        .order_by("caso__titulo", "id")
        .first()
    )

    if etapa and etapa.video:
        url = f"{reverse('simulacion:simulacion', args=[etapa.video.id])}?paciente_id={paciente.id}"
        return redirect(url)

    # Si el paciente no tiene una etapa con video, avisamos y regresamos al curso
    messages.warning(request, "Paciente no disponible, esperar por favor.")
    return redirect("curso:curso_detalle", curso_id=curso.id)
