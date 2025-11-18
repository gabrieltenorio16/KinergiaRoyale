from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, CreateView
from django.urls import reverse_lazy
from django.forms import modelform_factory
from django.contrib import messages
from django.db.models import Prefetch

from applications.Contenido.models import Video, Tema
from applications.diagnostico_paciente.models import Paciente, Etapa
from .models import Curso, SeleccionPacienteCurso


# -------------------------
# VISTAS QUE YA TENÍAS
# -------------------------
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


# -------------------------
# NUEVA PANTALLA DEL CURSO
# -------------------------

def curso_detalle(request, curso_id):
    """
    Pantalla del curso:
    - Fechas del curso
    - Índice: Temas -> Videos -> Preguntas
    - Pacientes de ejemplo
    - Contenidos adicionales (Etapas)
    """

    # 🔒 Si NO está logueado, lo mandamos a login_estudiantes (usuario/login/)
    if not request.user.is_authenticated:
        # 'login_estudiantes' es el name de tu URL de login en applications.usuario.urls
        return redirect("login_estudiantes")

    curso = get_object_or_404(Curso, pk=curso_id)

    # Temas del curso con videos y preguntas
    temas = (
        Tema.objects.filter(curso=curso)
        .prefetch_related(
            Prefetch('video_set', queryset=Video.objects.prefetch_related('preguntas'))
        )
        .order_by('titulo')
    )

    # Pacientes asociados al curso vía casos clínicos
    pacientes = (
        Paciente.objects.filter(casos_clinicos__curso=curso)
        .distinct()
        .order_by('apellidos', 'nombres')
    )

    # Selección actual del usuario (si ya escogió paciente para este curso)
    seleccion = (
        SeleccionPacienteCurso.objects
        .filter(usuario=request.user, curso=curso)
        .select_related('paciente')
        .first()
    )

    # Contenidos adicionales: etapas de los casos clínicos del curso
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


def seleccionar_paciente_curso(request, curso_id, paciente_id):
    """
    El estudiante selecciona un paciente de ejemplo dentro del curso.
    """

    # 🔒 Igual que arriba: si no está logueado, mandamos a login_estudiantes
    if not request.user.is_authenticated:
        return redirect("login_estudiantes")

    curso = get_object_or_404(Curso, pk=curso_id)

    # Solo pacientes que tengan caso clínico en este curso
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
    return redirect("curso_detalle", curso_id=curso.id)
