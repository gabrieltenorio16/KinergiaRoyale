from django.shortcuts import render, get_object_or_404
from applications.curso_y_modulo.models import Curso, ContenidoAsignado, SeleccionPacienteCurso
from applications.diagnostico_paciente.models import Paciente


def ver_curso(request, curso_id):
    curso = get_object_or_404(Curso, id=curso_id)
    estudiante = request.user  # estudiante logueado

    # pestaña activa (por si después quieres usar ?view=algo)
    active_view = request.GET.get("view", "presentacion")

    # ---------- ÍNDICE: CONTENIDOS ASIGNADOS ----------
    asignados = (
        ContenidoAsignado.objects
        .filter(curso=curso, estudiante=estudiante)
        .select_related("tema", "video")
        .order_by("tema__titulo", "video__titulo")
    )

    indice = {}
    for asignacion in asignados:
        tema = asignacion.tema
        video = asignacion.video
        if not tema:
            continue

        if tema not in indice:
            indice[tema] = []

        if video:
            indice[tema].append(video)

    # ---------- SALA DE ESPERA: PACIENTES ----------
    # Pacientes disponibles (simple: todos los pacientes; si después quieres filtrarlos por curso, se puede afinar)
    pacientes = Paciente.objects.all().order_by("apellidos", "nombres")

    # Paciente actualmente seleccionado por este estudiante en este curso
    seleccion = (
        SeleccionPacienteCurso.objects
        .filter(usuario=estudiante, curso=curso)
        .select_related("paciente")
        .first()
    )

    context = {
        "curso": curso,
        "active": active_view,
        "indice": indice,
        "pacientes": pacientes,
        "seleccion": seleccion,
    }

    # OJO: ajusta la ruta al template si tu carpeta es "curso" o "cursos"
    return render(request, "curso/curso_detalle.html", context)

