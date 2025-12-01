# applications/curso_y_modulo/views/estudiante.py

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.db.models import Prefetch

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
        .order_by('caso', 'orden')
    )

    context = {
        "curso": curso,
        "temas": temas,
        "pacientes": pacientes,
        "seleccion": seleccion,
        "etapas": etapas,
        "secciones_menu": ["fechas", "indice", "pacientes", "contenidos"],
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

    paciente = get_object_or_404(
        Paciente,
        pk=paciente_id,
        casos_clinicos__curso=curso
    )

    SeleccionPacienteCurso.objects.update_or_create(
        usuario=request.user,
        curso=curso,
        defaults={"paciente": paciente},
    )

    messages.success(request, f"Paciente seleccionado: {paciente}")

    primer_video = (
        Video.objects.filter(tema__curso=curso)
        .order_by('tema__titulo', 'id')
        .first()
    )

    if primer_video:
        return redirect("curso_y_modulo:simulacion", pk=primer_video.id)

    return redirect("curso_y_modulo:curso_detalle", curso_id=curso.id)
