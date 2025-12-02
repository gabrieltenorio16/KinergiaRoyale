<<<<<<< Updated upstream
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import DetailView, CreateView
from django.urls import reverse_lazy
from django.forms import modelform_factory
from django.contrib import messages
from django.db.models import Prefetch

from applications.Contenido.models import Video, Tema
from applications.diagnostico_paciente.models import Paciente, Etapa, CasoClinico
from .models import Curso, SeleccionPacienteCurso


# -------------------------
# VISTAS DE VIDEO SIMULACIÓN
# -------------------------
# 🚨 1. RENOMBRAR Y RECONFIGURAR LA VISTA DE DETALLE
class EtapaDetailView(DetailView):
    # Cambiamos el modelo a Etapa y el nombre del contexto
    model = Etapa
    template_name = "video/video_simulacion.html"
    context_object_name = "etapa" # Ahora la plantilla recibe 'etapa'
    pk_url_kwarg = 'pk' # La URL debe pasar el ID de la etapa como 'pk'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        etapa = self.object # El objeto Etapa actual
        
        # Obtenemos el Paciente asociado a esta Etapa a través del Caso Clínico
        paciente = None
        # Asumimos que Etapa tiene un FK llamado 'caso'
        if hasattr(etapa, 'caso'):
             # Asumimos que CasoClinico tiene un FK llamado 'paciente'
             paciente = etapa.caso.paciente 
        
        context["paciente_actual"] = paciente
        
        # La lógica del formulario de paciente (si la usas) se mantiene:
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
        return reverse_lazy("curso_y_modulo:simulacion_video", kwargs={"pk": self.kwargs["pk"]})


# -------------------------
# NUEVA PANTALLA DEL CURSO
# -------------------------

def curso_detalle(request, curso_id):
    """
    Pantalla del curso (vista pensada para el ESTUDIANTE):
    - Fechas del curso
    - Índice: Temas -> Videos -> Preguntas
    - Pacientes de ejemplo asociados al curso
    - Contenidos adicionales (Etapas)
    """

    # 🔒 Si NO está logueado, lo mandamos al login de estudiantes
    if not request.user.is_authenticated:
        # 'login_estudiantes' es el name de tu URL de login en applications.usuario.urls
        return redirect("usuario:login_estudiantes")

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


# applications/curso_y_modulo/views.py

def seleccionar_paciente_curso(request, curso_id, paciente_id):
    """
    El estudiante selecciona un paciente de ejemplo y se redirige 
    a la PRIMERA Etapa de ese caso clínico.
    """
    
    # 1. Verificación de Login
    if not request.user.is_authenticated:
        messages.error(request, "Debes iniciar sesión para seleccionar un paciente.")
        return redirect("usuario:login_estudiantes")

    curso = get_object_or_404(Curso, pk=curso_id)

    # 2. Obtener Paciente
    paciente = get_object_or_404(
        Paciente,
        pk=paciente_id,
        casos_clinicos__curso=curso
    )

    # 3. Guardar la selección
    SeleccionPacienteCurso.objects.update_or_create(
        usuario=request.user,
        curso=curso,
        defaults={"paciente": paciente},
    )

    messages.success(request, f"Paciente seleccionado: {paciente}")

    # ------------------------------------------------------------------
    # 🔥 NUEVA LÓGICA: Redirigir a la primera ETAPA del Caso Clínico
    # ------------------------------------------------------------------
    
    # A. Buscar el caso clínico asociado a este paciente y curso
    # (Asumiendo que Paciente tiene related_name='casos_clinicos')
    caso_asociado = paciente.casos_clinicos.filter(curso=curso).first() 

    if caso_asociado:
        # B. Buscar la primera Etapa (orden=1) de ese Caso
        initial_etapa = Etapa.objects.filter(
            caso=caso_asociado, 
            orden=1 
        ).first()

        if initial_etapa:
            # C. ¡ÉXITO! Redirigir a la vista de simulación con el ID de la ETAPA
            return redirect("curso_y_modulo:simulacion_video", pk=initial_etapa.pk)

    # ------------------------------------------------------------------
    # Fallback si no se encuentra la Etapa
    messages.error(request, "No se encontró la Etapa inicial para este caso clínico.")
    return redirect("curso_y_modulo:curso_detalle", curso_id=curso.id)
=======
# Este archivo ya no se usa.
# Las vistas fueron movidas a la carpeta views/


>>>>>>> Stashed changes
def ver_curso(request, curso_id):
    curso = Curso.objects.get(id=curso_id)

    view = request.GET.get("view", "presentacion")

    temas = curso.temas.all() if hasattr(curso, 'temas') else None

    context = {
        'curso': curso,
        'temas': temas,
        'active': view,
    }

    return render(request, "cursos/curso_detalle.html", context)
