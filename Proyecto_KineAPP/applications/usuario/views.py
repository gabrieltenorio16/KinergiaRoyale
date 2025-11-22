from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model

from applications.diagnostico_paciente.models import Etapa
from applications.Contenido.models import Historial


# Importamos los modelos
from .models import Estudiante

User = get_user_model()

# ==========================================
# 1. VISTA DE ESTUDIANTE (DASHBOARD)
# ==========================================
def panel_estudiante(request):
    user = request.user

    # 1) Obtener los cursos en los que el usuario está inscrito como estudiante
    cursos_activos = user.cursos_como_estudiante.all()

    # 2) Enriquecer cada curso con indicadores calculados
    for curso in cursos_activos:
        # --- Indicador 1: Casos clínicos asignados al curso ---
        # Usa la relación Curso -> CasoClinico (related_name='casos_clinicos')
        total_casos = curso.casos_clinicos.count()
        curso.total_casos_visibles = total_casos

        # --- Indicador 2: Progreso del curso ---
        # Total de etapas clínicas que tiene el curso (todas las etapas de todos los casos del curso)
        total_etapas = Etapa.objects.filter(caso__curso=curso).count()

        # Etapas (o registros clínicos) completadas por el estudiante
        # Usamos Historial como proxy de "avance", ligado a Tema y Curso
        etapas_completadas = Historial.objects.filter(
            tema__curso=curso,
            estudiante=user,
        ).count()

        if total_etapas > 0:
            progreso = int((etapas_completadas / total_etapas) * 100)
        else:
            progreso = 0

        curso.progreso_calculado = progreso

    context = {
        "perfil": user,
        "cursos_activos": cursos_activos,
    }

    return render(request, "inicio/home.html", context)



# ==========================================
# 2. LOGIN
# ==========================================
def login_estudiantes(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        # --- Caso 1: Usuario no existe ---
        from django.contrib.auth import get_user_model
        User = get_user_model()

        if not User.objects.filter(username=username).exists():
            messages.error(request, "No existe el usuario, por favor regístrese.")
            return redirect("usuario:login_estudiantes")

        # --- Caso 2: Usuario existe pero contraseña incorrecta ---
        if user is None:
            messages.error(request, "La contraseña es incorrecta.")
            return redirect("usuario:login_estudiantes")

        # --- Caso 3: Usuario existe, pero no tiene el rol adecuado ---
        if not (user.rol == "EST" or user.is_staff):
            messages.error(request, "Este usuario no tiene acceso como estudiante.")
            return redirect("usuario:login_estudiantes")

        # --- Caso 4: Usuario válido ---
        login(request, user)
        return redirect("usuario:panel_estudiante")

    return render(request, "login/login.html")



# ==========================================
# 3. REGISTRO
# ==========================================
def register_view(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        rut = request.POST.get("rut")
        email = request.POST.get("email")
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, "login/register.html")

        if User.objects.filter(username=username).exists():
            messages.error(request, "El usuario ya existe.")
            return render(request, "login/register.html")

        user = User.objects.create_user(
            username=username, email=email, password=password1,
            first_name=first_name, last_name=last_name, rut=rut
        )
        user.rol = "EST"
        user.save()

        # Creamos el perfil automáticamente
        Estudiante.objects.create(usuario=user)

        messages.success(request, "Cuenta creada. Inicia sesión.")
        return redirect("usuario:login_estudiantes")

    return render(request, "login/register.html")


def redirect_to_login(request):
    return redirect("usuario:login_estudiantes")


# ==========================================
# 4. RECUPERACIÓN DE CONTRASEÑA
# ==========================================
def forgot_password_view(request):
    if request.method == "POST":
        email = request.POST.get("email")
        if not User.objects.filter(email=email).exists():
            messages.error(request, "No existe una cuenta con ese correo.")
            return render(request, "login/forgot_password.html")
        
        return redirect("usuario:forgot_password") # O una pantalla de éxito

    return render(request, "login/forgot_password.html")


def email_sent_view(request):
    return render(request, "login/email_sent.html")