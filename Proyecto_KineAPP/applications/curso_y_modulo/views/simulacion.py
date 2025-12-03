# applications/curso_y_modulo/views/simulacion.py

from django.forms import modelform_factory
from django.urls import reverse_lazy
from django.views.generic import DetailView, CreateView

from applications.Contenido.models import Video, Topico, Pregunta, Respuesta
from applications.diagnostico_paciente.models import Paciente


class VideoDetailView(DetailView):
    model = Video
    template_name = "video/video_simulacion.html"
    context_object_name = "video"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

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
            Respuesta.objects.values("id", "contenido", "es_correcta", "pregunta_id").order_by("pregunta_id", "id")
        )
        return context


class FichaPacienteCreate(CreateView):
    model = Paciente
    fields = ["nombres", "apellidos", "edad", "antecedentes", "historial_medico"]
    template_name = "video/video_simulacion.html"

    def get_success_url(self):
        return reverse_lazy("simulacion", kwargs={"pk": self.kwargs["pk"]})
