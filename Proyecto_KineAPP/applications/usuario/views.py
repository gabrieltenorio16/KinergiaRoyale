from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth import get_user_model

# Importamos los modelos
from .models import Estudiante, Modulo

User = get_user_model()

# ==========================================
# 1. VISTA DEL PANEL (DASHBOARD)
# ==========================================
@login_required
def panel_estudiante(request):
    user = request.user
    
    # Busca o crea el perfil del estudiante
    estudiante, created = Estudiante.objects.get_or_create(usuario=user)

    # Obtiene sus módulos
    modulos_activos = estudiante.modulos.all()

    # Lógica visual simple
    for modulo in modulos_activos:
        modulo.total_casos_visibles = 5 
        modulo.progreso_calculado = 85

    context = {
        'perfil': estudiante,
        'modulos_activos': modulos_activos
    }
    
    return render(request, "inicio/home.html", context)


# ==========================================
# 2. LOGIN
# ==========================================
def login_estudiantes(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        # ESTA ERA LA LÍNEA DEL ERROR (Ahora está alineada)
        user = authenticate(request, username=username, password=password)

        if user is not None:
            # Permitimos entrar si es Estudiante (EST) o Staff (Admin)
            if user.rol == "EST" or user.is_staff:
                login(request, user)
                return redirect("usuario:panel_estudiante")
            else:
                messages.error(request, "Este usuario no tiene rol de estudiante.")
        else:
            messages.error(request, "Credenciales inválidas.")

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