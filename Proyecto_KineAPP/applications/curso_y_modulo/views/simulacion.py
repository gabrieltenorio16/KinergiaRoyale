# applications/curso_y_modulo/views/simulacion.py

from django.db import transaction
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import DetailView
from django.http import JsonResponse
from django.urls import reverse

from applications.Contenido.models import Video, Topico, Pregunta, Respuesta
from applications.diagnostico_paciente.models import (
    Diagnostico,
    FichaClinicaEstudiante,
    Paciente,
    HistorialSimulacion,
)
from applications.curso_y_modulo.models import SeleccionPacienteCurso
from applications.Contenido.contenido_modulo_docente.forms import FichaClinicaEstudianteForm


def _resolver_paciente_y_etapa(video, request):
    """
    Determina el paciente y la etapa asociada al video tomando en cuenta
    el paciente seleccionado por el estudiante (querystring o selección guardada).
    """
    curso = getattr(getattr(video, "tema", None), "curso", None)
    selected_paciente_id = request.GET.get("paciente_id")

    if not selected_paciente_id and curso and request.user.is_authenticated:
        seleccion = (
            SeleccionPacienteCurso.objects.filter(usuario=request.user, curso=curso)
            .select_related("paciente")
            .first()
        )
        if seleccion and seleccion.paciente_id:
            selected_paciente_id = seleccion.paciente_id

    etapas_qs = (
        video.etapas.select_related("paciente", "caso", "caso__paciente")
        .order_by("id")
    )

    etapa = None
    paciente_actual = None

    if selected_paciente_id:
        etapa = etapas_qs.filter(
            Q(paciente_id=selected_paciente_id) | Q(caso__paciente_id=selected_paciente_id)
        ).first()
        paciente_actual = Paciente.objects.filter(pk=selected_paciente_id).first()

    if not etapa:
        etapa = etapas_qs.first()

    if not paciente_actual and etapa:
        paciente_actual = getattr(etapa, "paciente", None) or getattr(
            getattr(etapa, "caso", None), "paciente", None
        )

    return paciente_actual, etapa


class VideoDetailView(DetailView):
    model = Video
    template_name = "video/video_simulacion.html"
    context_object_name = "video"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        paciente_actual, etapa = _resolver_paciente_y_etapa(self.object, self.request)
        context["etapa"] = etapa
        context["paciente_actual"] = paciente_actual
        context["paciente"] = paciente_actual

        # ---------- FICHA CLÖNICA DEL ESTUDIANTE ----------
        ficha_existente = None
        if (
            self.request.user.is_authenticated
            and paciente_actual
            and etapa
            and etapa.caso
        ):
            ficha_existente = FichaClinicaEstudiante.objects.filter(
                estudiante=self.request.user,
                paciente=paciente_actual,
                caso_clinico=etapa.caso,
                video=self.object,
            ).first()

        if ficha_existente:
            context["ficha_form"] = FichaClinicaEstudianteForm(instance=ficha_existente)
            context["ficha_existente"] = ficha_existente
        else:
            # No prellenamos: el estudiante debe completarla
            context["ficha_form"] = FichaClinicaEstudianteForm()
        # --------------------------------------------------

        # Topicos y preguntas (para filtrar por t¢pico en la vista)
        context["topicos_data"] = list(
            Topico.objects.values("id", "nombre", "descripcion").order_by("nombre")
        )
        context["preguntas_data"] = list(
            Pregunta.objects.select_related("topico")
            .values("id", "pregunta", "topico_id")
            .order_by("topico_id", "id")
        )

        context["respuestas_data"] = list(
            Respuesta.objects.values(
                "id", "contenido", "retroalimentacion", "es_correcta", "pregunta_id"
            ).order_by("pregunta_id", "id")
        )

        diagnosticos_qs = Diagnostico.objects.none()
        if paciente_actual:
            diagnosticos_qs = (
                Diagnostico.objects.filter(paciente=paciente_actual)
                .select_related("caso", "parte_cuerpo")
                .order_by("id")
            )
            if etapa and etapa.caso_id:
                diagnosticos_qs = diagnosticos_qs.filter(
                    Q(caso=etapa.caso) | Q(caso__isnull=True)
                )

        context["diagnosticos_data"] = [
            {
                "id": diag.id,
                "descripcion": diag.descripcion or "",
                "caso": diag.caso.titulo if diag.caso else "",
                "parte_cuerpo": diag.parte_cuerpo.nombre if diag.parte_cuerpo else "",
            }
            for diag in diagnosticos_qs
        ]

        # URL para registrar respuestas vía fetch
        context["registrar_respuesta_url"] = reverse(
            "simulacion:registrar_respuesta", args=[self.object.pk]
        )

        return context


@login_required
def guardar_ficha_clinica_estudiante(request, pk):
    video = get_object_or_404(Video, pk=pk)
    paciente_actual, etapa = _resolver_paciente_y_etapa(video, request)
    caso_clinico = etapa.caso if etapa else None

    if request.method != "POST":
        return redirect("simulacion:simulacion", pk=video.pk)

    if not paciente_actual or not caso_clinico:
        messages.error(request, "No hay un paciente/caso asociado a este video.")
        return redirect("simulacion:simulacion", pk=video.pk)

    ficha_existente = FichaClinicaEstudiante.objects.filter(
        estudiante=request.user,
        paciente=paciente_actual,
        caso_clinico=caso_clinico,
        video=video,
    ).first()

    if ficha_existente:
        form = FichaClinicaEstudianteForm(request.POST, instance=ficha_existente)
    else:
        form = FichaClinicaEstudianteForm(request.POST)

    if form.is_valid():
        with transaction.atomic():
            ficha = form.save(commit=False)
            ficha.estudiante = request.user
            ficha.paciente = paciente_actual
            ficha.caso_clinico = caso_clinico
            ficha.video = video
            ficha.save()

            historial, _ = HistorialSimulacion.objects.get_or_create(
                estudiante=request.user,
                video=video,
                paciente=paciente_actual,
                caso_clinico=caso_clinico,
                defaults={"ficha": ficha},
            )
            if historial.ficha_id != ficha.id:
                historial.ficha = ficha
                historial.save(update_fields=["ficha", "updated_at"])
        messages.success(request, "Ficha cl¡nica guardada correctamente.")
    else:
        messages.error(request, f"Errores en la ficha: {form.errors}")

    return redirect("simulacion:simulacion", pk=video.pk)


@login_required
def registrar_respuesta(request, pk):
    """
    Registra si una respuesta fue correcta o incorrecta en el historial del estudiante.
    """
    if request.method != "POST":
        return JsonResponse({"error": "Método no permitido"}, status=405)

    video = get_object_or_404(Video, pk=pk)
    paciente_actual, etapa = _resolver_paciente_y_etapa(video, request)
    caso_clinico = etapa.caso if etapa else None

    if not paciente_actual or not caso_clinico:
        return JsonResponse(
            {"error": "No hay paciente/caso asociado a este video para el usuario."},
            status=400,
        )

    respuesta_id = request.POST.get("respuesta_id")
    pregunta_id = request.POST.get("pregunta_id")

    if not respuesta_id or not pregunta_id:
        return JsonResponse({"error": "Falta pregunta o respuesta."}, status=400)

    respuesta = Respuesta.objects.filter(pk=respuesta_id, pregunta_id=pregunta_id).first()
    if not respuesta:
        return JsonResponse({"error": "Respuesta no encontrada."}, status=404)

    historial, _ = HistorialSimulacion.objects.get_or_create(
        estudiante=request.user,
        video=video,
        paciente=paciente_actual,
        caso_clinico=caso_clinico,
    )

    campo = "respuestas_correctas" if respuesta.es_correcta else "respuestas_incorrectas"
    setattr(historial, campo, getattr(historial, campo) + 1)
    historial.save(update_fields=[campo, "updated_at"])

    return JsonResponse({"ok": True, "correcta": respuesta.es_correcta})
