# applications/curso_y_modulo/views/simulacion.py

from django.db.models import Q
from django.forms import modelform_factory
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView

from applications.Contenido.models import Video, Topico, Pregunta, Respuesta
from applications.diagnostico_paciente.models import Paciente, Diagnostico


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

        PacienteForm = modelform_factory(
            Paciente,
            fields=["nombres", "apellidos", "edad", "antecedentes", "historial_medico"],
        )

        context["form"] = PacienteForm()

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


class FichaPacienteCreate(CreateView):
    model = Paciente
    fields = ["nombres", "apellidos", "edad", "antecedentes", "historial_medico"]
    template_name = "video/video_simulacion.html"

    def get_success_url(self):
        return reverse_lazy("simulacion", kwargs={"pk": self.kwargs["pk"]})
