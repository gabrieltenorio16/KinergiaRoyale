# applications/curso_y_modulo/views/simulacion.py

from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.views.generic import DetailView

from applications.Contenido.models import Video, Topico, Pregunta, Respuesta
from applications.diagnostico_paciente.models import Diagnostico, FichaClinicaEstudiante
from applications.Contenido.contenido_modulo_docente.forms import FichaClinicaEstudianteForm


class VideoDetailView(DetailView):
    model = Video
    template_name = "video/video_simulacion.html"
    context_object_name = "video"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        etapa = (
            self.object.etapas.select_related("paciente", "caso__paciente")
            .order_by("id")
            .first()
        )
        context["etapa"] = etapa

        paciente_actual = None
        if etapa:
            if getattr(etapa, "paciente", None):
                paciente_actual = etapa.paciente
            elif getattr(etapa, "caso", None) and getattr(etapa.caso, "paciente", None):
                paciente_actual = etapa.caso.paciente
        context["paciente_actual"] = paciente_actual
        context["paciente"] = paciente_actual

         # ---------- FICHA CLÍNICA DEL ESTUDIANTE ----------
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
            initial = {}
            if paciente_actual:
                initial = {
                    "nombre_paciente_ficha": paciente_actual.nombres,
                    "apellido_paciente_ficha": paciente_actual.apellidos,
                    "edad_paciente_ficha": paciente_actual.edad,
                }
            context["ficha_form"] = FichaClinicaEstudianteForm(initial=initial)
        # --------------------------------------------------

        # Topicos y preguntas (para filtrar por tópico en la vista)
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

        return context


@login_required
def guardar_ficha_clinica_estudiante(request, pk):
    video = get_object_or_404(Video, pk=pk)

    # Reutilizamos la misma lógica para etapa/paciente/caso
    etapa = (
        video.etapas.select_related("paciente", "caso__paciente")
        .order_by("id")
        .first()
    )

    paciente_actual = None
    caso_clinico = None
    if etapa:
        caso_clinico = etapa.caso
        if getattr(etapa, "paciente", None):
            paciente_actual = etapa.paciente
        elif getattr(etapa, "caso", None) and getattr(etapa.caso, "paciente", None):
            paciente_actual = etapa.caso.paciente

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
        ficha = form.save(commit=False)
        ficha.estudiante = request.user
        ficha.paciente = paciente_actual
        ficha.caso_clinico = caso_clinico
        ficha.video = video
        ficha.save()
        messages.success(request, "Ficha clínica guardada correctamente.")
    else:
        messages.error(request, f"Errores en la ficha: {form.errors}")


    return redirect("simulacion:simulacion", pk=video.pk)