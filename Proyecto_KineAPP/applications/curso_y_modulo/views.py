from django.shortcuts import render
from applications.Contenido.models import Video
from django.views.generic import DetailView, CreateView
from applications.diagnostico_paciente.models import Paciente
from django.urls import reverse_lazy
from django.forms import modelform_factory

class VideoDetailView(DetailView):
    model = Video
    template_name = "video/video_simulacion.html"
    context_object_name = "video"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        PacienteForm = modelform_factory(
            Paciente,
            fields=["nombres", "apellidos", "edad", "antecedentes", "historial_medico"]
        )

        context["form"] = PacienteForm()
        return context

class FichaPacienteCreate(CreateView):
    model = Paciente
    fields = ["nombres", "apellidos", "edad", "antecedentes", "historial_medico"]
    template_name = "video/video_simulacion.html"

    def get_success_url(self):
        return reverse_lazy("simulacion", kwargs={"pk": self.kwargs["pk"]})
    

