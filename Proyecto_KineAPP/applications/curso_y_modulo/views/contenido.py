from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from applications.curso_y_modulo.models import Curso
from applications.Contenido.models import Tema, Video, Topico, Pregunta, Respuesta
from applications.diagnostico_paciente.models import (
    Paciente,
    ParteCuerpo,
    CasoClinico,
    Etapa,
    Diagnostico,
    FichaClinicaEstudiante,
)
from applications.Contenido.contenido_modulo_docente.forms import (
    TemaForm,
    VideoForm,
    TopicoForm,
    PreguntaForm,
    RespuestaForm,
    PacienteForm,
    CasoClinicoForm,
    EtapaForm
)


@login_required
def asignar_contenido(request, curso_id):
    """
    Pantalla de asignación de contenido para un curso:
    - CRUD de Temas (filtrados por curso)
    - CRUD de Videos (filtrados por curso vía Tema)
    - CRUD de Tópicos (globales, banco de contenido)
    - CRUD de Preguntas (globales, banco de contenido)
    """

    if request.user.rol != "DOC":
        messages.error(request, "No tienes permisos para acceder a esta sección.")
        return redirect("root_redirect")

    curso = get_object_or_404(Curso, pk=curso_id)

    temas = Tema.objects.filter(curso=curso).order_by("titulo")
    videos = (
        Video.objects
        .filter(tema__curso=curso)
        .select_related("tema")
        .order_by("tema__titulo", "titulo")
    )
    topicos = (
        Topico.objects
        .prefetch_related("preguntas")
        .order_by("nombre")
    )
    preguntas = (
        Pregunta.objects
        .select_related("topico")
        .order_by("topico__nombre", "id")
    )

    respuestas = (
    Respuesta.objects
    .select_related("pregunta", "pregunta__topico")
    .order_by("pregunta__topico__nombre", "pregunta_id", "id")
)

    tema_form = TemaForm()
    video_form = get_video_form(curso)
    topico_form = TopicoForm()
    pregunta_form = PreguntaForm()
    respuesta_form = RespuestaForm()

    if request.method == "POST":
        tipo = request.POST.get("tipo", "tema")       # tema | video | topico | pregunta
        accion = request.POST.get("accion", "crear")  # crear | editar | eliminar

        # =========================================================
        # TEMAS
        # =========================================================
        if tipo == "tema":
            if accion == "eliminar":
                ids = request.POST.getlist("temas_seleccionados")
                if not ids:
                    messages.warning(request, "No seleccionaste ningún tema para borrar.")
                else:
                    Tema.objects.filter(curso=curso, id__in=ids).delete()
                    messages.success(request, "Temas eliminados correctamente.")
                return redirect("docente:asignar_contenido", curso_id=curso.id)

            elif accion == "editar":
                tema_id = request.POST.get("tema_id")
                tema_obj = get_object_or_404(Tema, pk=tema_id, curso=curso)
                form = TemaForm(request.POST, instance=tema_obj)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Tema actualizado correctamente.")
                    return redirect("docente:asignar_contenido", curso_id=curso.id)
                else:
                    messages.error(request, "Revisa los datos del tema.")
                    tema_form = form

            else:  # crear tema
                form = TemaForm(request.POST)
                if form.is_valid():
                    tema = form.save(commit=False)
                    tema.curso = curso
                    tema.save()
                    messages.success(request, "Tema creado correctamente.")
                    return redirect("docente:asignar_contenido", curso_id=curso.id)
                else:
                    messages.error(request, "Revisa los datos del nuevo tema.")
                    tema_form = form

        # =========================================================
        # VIDEOS
        # =========================================================
        elif tipo == "video":
            if accion == "eliminar":
                ids = request.POST.getlist("videos_seleccionados")
                if not ids:
                    messages.warning(request, "No seleccionaste ningún video para borrar.")
                else:
                    Video.objects.filter(tema__curso=curso, id__in=ids).delete()
                    messages.success(request, "Videos eliminados correctamente.")
                return redirect("docente:asignar_contenido", curso_id=curso.id)

            elif accion == "editar":
                video_id = request.POST.get("video_id")
                video_obj = get_object_or_404(Video, pk=video_id, tema__curso=curso)
                form = get_video_form(curso, request.POST, instance=video_obj)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Video actualizado correctamente.")
                    return redirect("docente:asignar_contenido", curso_id=curso.id)
                else:
                    messages.error(request, "Revisa los datos del video.")
                    video_form = form

            else:  # crear video
                form = get_video_form(curso, request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Video creado correctamente.")
                    return redirect("docente:asignar_contenido", curso_id=curso.id)
                else:
                    messages.error(request, "Revisa los datos del nuevo video.")
                    video_form = form

        # =========================================================
        # TÓPICOS
        # =========================================================
        elif tipo == "topico":
            if accion == "eliminar":
                ids = request.POST.getlist("topicos_seleccionados")
                if not ids:
                    messages.warning(request, "No seleccionaste ningún tópico para borrar.")
                else:
                    Topico.objects.filter(id__in=ids).delete()
                    messages.success(request, "Tópicos eliminados correctamente.")
                return redirect("docente:asignar_contenido", curso_id=curso.id)

            elif accion == "editar":
                topico_id = request.POST.get("topico_id")
                topico_obj = get_object_or_404(Topico, pk=topico_id)
                form = TopicoForm(request.POST, instance=topico_obj)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Tópico actualizado correctamente.")
                    return redirect("docente:asignar_contenido", curso_id=curso.id)
                else:
                    messages.error(request, "Revisa los datos del tópico.")
                    topico_form = form

            else:  # crear tópico
                form = TopicoForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Tópico creado correctamente.")
                    return redirect("docente:asignar_contenido", curso_id=curso.id)
                else:
                    messages.error(request, "Revisa los datos del nuevo tópico.")
                    topico_form = form

        # =========================================================
        # PREGUNTAS
        # =========================================================
        elif tipo == "pregunta":
            if accion == "eliminar":
                ids = request.POST.getlist("preguntas_seleccionadas")
                if not ids:
                    messages.warning(request, "No seleccionaste ninguna pregunta para borrar.")
                else:
                    Pregunta.objects.filter(id__in=ids).delete()
                    messages.success(request, "Preguntas eliminadas correctamente.")
                return redirect("docente:asignar_contenido", curso_id=curso.id)

            elif accion == "editar":
                pregunta_id = request.POST.get("pregunta_id")
                pregunta_obj = get_object_or_404(Pregunta, pk=pregunta_id)
                form = PreguntaForm(request.POST, instance=pregunta_obj)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Pregunta actualizada correctamente.")
                    return redirect("docente:asignar_contenido", curso_id=curso.id)
                else:
                    messages.error(request, "Revisa los datos de la pregunta.")
                    pregunta_form = form

            else:  # crear pregunta
                form = PreguntaForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Pregunta creada correctamente.")
                    return redirect("docente:asignar_contenido", curso_id=curso.id)
                else:
                    messages.error(request, "Revisa los datos de la nueva pregunta.")
                    pregunta_form = form

        # =========================================================
        # RESPUESTAS
        # =========================================================
        elif tipo == "respuesta":
            if accion == "eliminar":
                ids = request.POST.getlist("respuestas_seleccionadas")
                if not ids:
                    messages.warning(request, "No seleccionaste ninguna respuesta para borrar.")
                else:
                    Respuesta.objects.filter(id__in=ids).delete()
                    messages.success(request, "Respuestas eliminadas correctamente.")
                return redirect("docente:asignar_contenido", curso_id=curso.id)

            elif accion == "editar":
                respuesta_id = request.POST.get("respuesta_id")
                respuesta_obj = get_object_or_404(Respuesta, pk=respuesta_id)
                form = RespuestaForm(request.POST, instance=respuesta_obj)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Respuesta actualizada correctamente.")
                    return redirect("docente:asignar_contenido", curso_id=curso.id)
                else:
                    messages.error(request, "Revisa los datos de la respuesta.")
                    respuesta_form = form

            else:  # crear respuesta
                form = RespuestaForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Respuesta creada correctamente.")
                    return redirect("docente:asignar_contenido", curso_id=curso.id)
                else:
                    messages.error(request, "Revisa los datos de la nueva respuesta.")
                    respuesta_form = form


    return render(request, "docente/asignar_contenido.html", {
        "curso": curso,
        "temas": temas,
        "videos": videos,
        "topicos": topicos,
        "preguntas": preguntas,
        "respuestas": respuestas,
        "tema_form": tema_form,
        "video_form": video_form,
        "topico_form": topico_form,
        "pregunta_form": pregunta_form,
        "respuesta_form": respuesta_form,
        "active_section": "contenido",
        "breadcrumb_label": "Contenido del módulo",
        "breadcrumb_url_name": "docente:asignar_contenido",
    })


def get_video_form(curso, *args, **kwargs):
    form = VideoForm(*args, **kwargs)
    form.fields["tema"].queryset = Tema.objects.filter(curso=curso).order_by("titulo")
    return form


@login_required
def asignar_pacientes(request, curso_id):

    if request.user.rol != "DOC":
        messages.error(request, "No tienes permisos para acceder a esta sección.")
        return redirect("root_redirect")

    curso = get_object_or_404(Curso, pk=curso_id)

    # Pacientes que tienen al menos un caso clínico asociado al curso
    pacientes = (
      Paciente.objects.all().order_by("apellidos", "nombres")
    )

    # Casos clínicos del curso
    casos_clinicos = (
        CasoClinico.objects.filter(curso=curso)
        .select_related("paciente")
        .order_by("-fecha_creacion")
    )

    # Etapas de los casos clínicos del curso
    etapas = (
        Etapa.objects.filter(caso__curso=curso)
        .select_related("caso", "paciente", "parte_cuerpo")
        .order_by("caso__titulo", "nombre")
    )

    # Diagnósticos asociados a pacientes que pertenecen al curso
    diagnosticos = (
        Diagnostico.objects.filter(paciente__casos_clinicos__curso=curso)
        .select_related("paciente", "caso")
        .order_by("caso__titulo", "paciente__apellidos", "id")
        .distinct()
    )


    # Partes del cuerpo disponibles (no se filtran por curso)
    partes_cuerpo = ParteCuerpo.objects.all().order_by("nombre")

    paciente_form = PacienteForm()
    caso_form = CasoClinicoForm()
    etapa_form = EtapaForm()

    if request.method == "POST":
        tipo = request.POST.get("tipo", "caso")       # paciente | caso | etapa
        accion = request.POST.get("accion", "crear")  # crear | editar | eliminar

        # ---------------------------------------------------------
        # PACIENTES
        # ---------------------------------------------------------
        if tipo == "paciente":
            if accion == "eliminar":
                ids = request.POST.getlist("pacientes_seleccionados")
                if not ids:
                    messages.warning(request, "No seleccionaste ningún paciente para borrar.")
                else:
                    Paciente.objects.filter(id__in=ids).delete()
                    messages.success(request, "Pacientes eliminados correctamente.")
                return redirect("docente:asignar_pacientes", curso_id=curso.id)

            elif accion == "editar":
                paciente_id = request.POST.get("paciente_id")
                paciente_obj = get_object_or_404(Paciente, pk=paciente_id)
                form = PacienteForm(request.POST, instance=paciente_obj)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Paciente actualizado correctamente.")
                    return redirect("docente:asignar_pacientes", curso_id=curso.id)
                else:
                    messages.error(request, "Revisa los datos del paciente.")
                    paciente_form = form

            else:  # crear paciente
                form = PacienteForm(request.POST)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Paciente creado correctamente.")
                    return redirect("docente:asignar_pacientes", curso_id=curso.id)
                else:
                    messages.error(request, "Revisa los datos del nuevo paciente.")
                    paciente_form = form

        # ---------------------------------------------------------
        # CASOS CLÍNICOS
        # ---------------------------------------------------------
        elif tipo == "caso":
            if accion == "eliminar":
                ids = request.POST.getlist("casos_seleccionados")
                if not ids:
                    messages.warning(request, "No seleccionaste ningún caso clínico para borrar.")
                else:
                    CasoClinico.objects.filter(curso=curso, id__in=ids).delete()
                    messages.success(request, "Casos clínicos eliminados correctamente.")
                return redirect("docente:asignar_pacientes", curso_id=curso.id)

            elif accion == "editar":
                caso_id = request.POST.get("caso_id")
                caso_obj = get_object_or_404(CasoClinico, pk=caso_id, curso=curso)
                form = CasoClinicoForm(request.POST, instance=caso_obj)
                if form.is_valid():
                    form.save()
                    messages.success(request, "Caso clínico actualizado correctamente.")
                    return redirect("docente:asignar_pacientes", curso_id=curso.id)
                else:
                    messages.error(request, "Revisa los datos del caso clínico.")
                    caso_form = form

            else:  # crear caso clínico
                form = CasoClinicoForm(request.POST)
                if form.is_valid():
                    caso = form.save(commit=False)
                    caso.curso = curso
                    caso.save()
                    messages.success(request, "Caso clínico creado correctamente.")
                    return redirect("docente:asignar_pacientes", curso_id=curso.id)
                else:
                    messages.error(request, "Revisa los datos del nuevo caso clínico.")
                    caso_form = form
        #---------------------------------------------------------
        # DIAGNOSTICOS 
        #--------------------------------------------------------
        elif tipo == "diagnostico":
            if accion == "eliminar":
                ids = request.POST.getlist("diagnosticos_seleccionados")
                if not ids:
                    messages.warning(request, "No seleccionaste ningún diagnóstico para borrar.")
                else:
                    Diagnostico.objects.filter(
                        id__in=ids,
                        paciente__casos_clinicos__curso=curso,
                    ).delete()
                    messages.success(request, "Diagnósticos eliminados correctamente.")
                return redirect("docente:asignar_pacientes", curso_id=curso.id)

            elif accion == "editar":
                diag_id = request.POST.get("diagnostico_id")
                diag = get_object_or_404(
                    Diagnostico,
                    pk=diag_id,
                    paciente__casos_clinicos__curso=curso,
                )
                paciente_id = request.POST.get("paciente")
                caso_id = request.POST.get("caso")
                descripcion = request.POST.get("descripcion", "").strip()

                if not paciente_id:
                    messages.error(request, "Debes seleccionar un paciente para el diagnóstico.")
                elif not caso_id:
                    messages.error(request, "Debes seleccionar el caso clínico asociado.")
                else:
                    caso = CasoClinico.objects.filter(
                        pk=caso_id,
                        curso=curso,
                        paciente_id=paciente_id,
                    ).first()
                    if not caso:
                        messages.error(
                            request,
                            "El caso clínico seleccionado no corresponde al paciente o al curso.",
                        )
                    else:
                        diag.paciente_id = paciente_id
                        diag.caso = caso
                        diag.descripcion = descripcion or None
                        diag.save()
                        messages.success(request, "Diagnóstico actualizado correctamente.")
                        return redirect("docente:asignar_pacientes", curso_id=curso.id)

            else:  # crear diagnóstico
                paciente_id = request.POST.get("paciente")
                caso_id = request.POST.get("caso")
                descripcion = request.POST.get("descripcion", "").strip()

                if not paciente_id:
                    messages.error(request, "Debes seleccionar un paciente para el diagnóstico.")
                elif not caso_id:
                    messages.error(request, "Debes seleccionar el caso clínico asociado.")
                else:
                    caso = CasoClinico.objects.filter(
                        pk=caso_id,
                        curso=curso,
                        paciente_id=paciente_id,
                    ).first()
                    if not caso:
                        messages.error(
                            request,
                            "El caso clínico seleccionado no corresponde al paciente o al curso.",
                        )
                    else:
                        Diagnostico.objects.create(
                            paciente_id=paciente_id,
                            caso=caso,
                            descripcion=descripcion or None,
                        )
                        messages.success(request, "Diagnóstico creado correctamente.")
                        return redirect("docente:asignar_pacientes", curso_id=curso.id)
        # ---------------------------------------------------------
        # ENTREVISTAS (Etapas)
        # ---------------------------------------------------------
        elif tipo == "etapa":
            if accion == "eliminar":
                ids = request.POST.getlist("etapas_seleccionadas")
                if not ids:
                    messages.warning(request, "No seleccionaste ninguna entrevista para borrar.")
                else:
                    Etapa.objects.filter(
                        caso__curso=curso,
                        id__in=ids,
                    ).delete()
                    messages.success(request, "Entrevistas eliminadas correctamente.")
                return redirect("docente:asignar_pacientes", curso_id=curso.id)

            elif accion == "editar":
                etapa_id = request.POST.get("etapa_id")
                etapa_obj = get_object_or_404(
                    Etapa,
                    pk=etapa_id,
                    caso__curso=curso,
                )
                form = EtapaForm(request.POST, instance=etapa_obj)
                if form.is_valid():
                    etapa = form.save(commit=False)
                    # aseguramos que el paciente coincida con el del caso
                    etapa.paciente = etapa.caso.paciente
                    etapa.save()
                    messages.success(request, "Entrevista actualizada correctamente.")
                    return redirect("docente:asignar_pacientes", curso_id=curso.id)
                else:
                    messages.error(request, "Revisa los datos de la entrevista.")
                    etapa_form = form

            else:  # crear entrevista
                form = EtapaForm(request.POST)
                if form.is_valid():
                    etapa = form.save(commit=False)
                    etapa.paciente = etapa.caso.paciente
                    etapa.save()
                    messages.success(request, "Entrevista creada correctamente.")
                    return redirect("docente:asignar_pacientes", curso_id=curso.id)
                else:
                    messages.error(request, "Revisa los datos de la nueva entrevista.")
                    etapa_form = form



    context = {
        "curso": curso,
        "pacientes": pacientes,
        "casos_clinicos": casos_clinicos,
        "etapas": etapas,
        "diagnosticos": diagnosticos,
        "partes_cuerpo": partes_cuerpo,
        "paciente_form": paciente_form,
        "caso_form": caso_form,
        "etapa_form": etapa_form,
        "active_section": "pacientes",
        "breadcrumb_label": "Pacientes",
        "breadcrumb_url_name": "docente:asignar_pacientes",
    }

    return render(request, "docente/asignar_pacientes.html", context)


@login_required
def fichas_clinicas_estudiantes(request, curso_id):
    """
    Lista las fichas clinicas que los estudiantes han creado para las
    simulaciones de video en este curso.
    """
    if request.user.rol != "DOC":
        messages.error(request, "No tienes permisos para acceder a esta seccion.")
        return redirect("root_redirect")

    curso = get_object_or_404(Curso, pk=curso_id)

    fichas = (
        FichaClinicaEstudiante.objects
        .filter(caso_clinico__curso=curso)
        .select_related("estudiante", "paciente", "caso_clinico", "video")
        .order_by("-fecha_creacion")
    )

    context = {
        "curso": curso,
        "fichas": fichas,
        "active_section": "fichas_estudiantes",
        "breadcrumb_label": "Fichas clinicas estudiantes",
        "breadcrumb_url_name": "docente:curso_fichas_estudiantes",
        "page_heading": "Fichas clinicas del curso",
        "page_subtitle": "Registros creados por los estudiantes en sus simulaciones.",
    }
    return render(request, "docente/fichas_clinicas_estudiantes.html", context)
