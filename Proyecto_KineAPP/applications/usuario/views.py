from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings

# Importación correcta del CustomUser
from django.contrib.auth import get_user_model
User = get_user_model()


def login_estudiantes(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None and user.rol == "EST":
            login(request, user)
            return redirect("panel_estudiante")
        else:
            messages.error(request, "Credenciales inválidas o usuario sin rol de estudiante.")

    return render(request, "login/login.html")


def redirect_to_login(request):
    return redirect("login_estudiantes")


def register_view(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name")
        last_name = request.POST.get("last_name")
        rut = request.POST.get("rut")               # 👈 NECESARIO
        email = request.POST.get("email")
        username = request.POST.get("username")
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # Validar contraseñas
        if password1 != password2:
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, "login/register.html")

        # Verificar duplicados
        if User.objects.filter(username=username).exists():
            messages.error(request, "El usuario ya está registrado.")
            return render(request, "login/register.html")

        if User.objects.filter(email=email).exists():
            messages.error(request, "El correo ya está asociado a una cuenta.")
            return render(request, "login/register.html")

        if User.objects.filter(rut=rut).exists():
            messages.error(request, "El RUT ya está asociado a una cuenta.")
            return render(request, "login/register.html")

        # Crear usuario con todos los campos requeridos
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name,
            rut=rut      # 👈 NECESARIO
        )

        # Asignar rol estudiante
        user.rol = "EST"
        user.save()

        messages.success(request, "Cuenta creada con éxito. Ahora puedes iniciar sesión.")
        return redirect("login_estudiantes")

    return render(request, "login/register.html")


def forgot_password_view(request):
    if request.method == "POST":
        email = request.POST.get("email")

        if not User.objects.filter(email=email).exists():
            messages.error(request, "No existe una cuenta con ese correo.")
            return render(request, "login/forgot_password.html")

        # Lógica real de correo se agregará después
        return redirect("email_sent")

    return render(request, "login/forgot_password.html")


def email_sent_view(request):
    return render(request, "login/email_sent.html")
