from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.exceptions import ValidationError
from django.contrib.auth.password_validation import validate_password
from django.template.loader import render_to_string

from applications.diagnostico_paciente.models import Etapa

from .models import Estudiante, Usuario

import re

User = get_user_model()


# =====================================================
#  FUNCIONES AUXILIARES
# =====================================================

def validar_rut_chileno(rut: str) -> bool:
    """
    Valida un RUT chileno. Acepta formatos con puntos y guión.
    Ej: 12.345.678-9
    """
    if not rut:
        return False

    rut = rut.replace(".", "").replace("-", "").upper().strip()

    if len(rut) < 8:
        return False

    cuerpo = rut[:-1]
    dv = rut[-1]

    if not cuerpo.isdigit():
        return False

    suma = 0
    multiplo = 2

    for digito in reversed(cuerpo):
        suma += int(digito) * multiplo
        multiplo += 1
        if multiplo == 8:
            multiplo = 2

    resto = suma % 11
    dv_esperado = 11 - resto

    if dv_esperado == 11:
        dv_esperado = "0"
    elif dv_esperado == 10:
        dv_esperado = "K"
    else:
        dv_esperado = str(dv_esperado)

    return dv == dv_esperado


# =====================================================
#  CONTEXTO COMÚN PARA VISTAS DE ESTUDIANTE
# =====================================================

def obtener_contexto_estudiante(user):
    """
    Devuelve el perfil y los cursos activos con el progreso calculado.
    Se usa en panel_estudiante, cursos_estudiante y casos_estudiante.
    """
    cursos_activos = user.cursos_como_estudiante.all()

    for curso in cursos_activos:
        # Indicador 1: Casos clínicos asignados al curso
        total_casos = curso.casos_clinicos.count()
        curso.total_casos_visibles = total_casos

        # Indicador 2: Progreso del curso
        total_etapas = Etapa.objects.filter(caso__curso=curso).count()
        # Si se desea progreso real, reintroducir modelo Historial y su consulta.
        etapas_completadas = 0

        if total_etapas > 0:
            progreso = int((etapas_completadas / total_etapas) * 100)
        else:
            progreso = 0

        curso.progreso_calculado = progreso

    return {
        "perfil": user,
        "cursos_activos": cursos_activos,
    }


# =====================================================
# 0. SELECCIONAR TIPO DE ENTRADA
# =====================================================

def seleccionar_entrada(request):
    """
    Pantalla inicial de /usuario/ donde eliges:
    - Staff  -> lleva a seleccionar_staff
    - Estudiante -> login de estudiante
    """
    return render(request, "login/seleccionar_entrada.html")


def seleccionar_staff(request):
    """
    Pantalla intermedia para elegir tipo de acceso Staff:
    - Administrador
    - Docente
    """
    return render(request, "login/seleccionar_staff.html")


# =====================================================
# 1. PANEL ESTUDIANTE - INICIO (NUEVO)
# =====================================================

@login_required
def panel_estudiante(request):
    """
    Nuevo INICIO del estudiante.
    Muestra saludo y un pequeño resumen.
    """
    context = obtener_contexto_estudiante(request.user)
    return render(request, "inicio/inicio_estudiante.html", context)


# =====================================================
# 1.1 PÁGINA DE CURSOS (usa tu HTML antiguo de inicio)
# =====================================================

@login_required
def cursos_estudiante(request):
    """
    Página de CURSOS activos del estudiante.
    Utiliza el template con la lista de cursos.
    """
    context = obtener_contexto_estudiante(request.user)
    return render(request, "inicio/cursos_estudiante.html", context)


# =====================================================
# 1.2 PÁGINA DE CASOS CLÍNICOS
# =====================================================

@login_required
def casos_estudiante(request):
    """
    Página de CASOS CLÍNICOS para el estudiante.
    De momento es básica; se puede enriquecer luego con datos reales.
    """
    context = obtener_contexto_estudiante(request.user)
    return render(request, "inicio/casos_estudiantes.html", context)


# =====================================================
# 2. LOGIN ESTUDIANTES (usuario O correo)
# =====================================================

def login_estudiantes(request):
    if request.method == "POST":
        identificador = request.POST.get("username")  # puede ser usuario O correo
        password = request.POST.get("password")

        UserModel = get_user_model()

        # Intentamos encontrar al usuario por username primero
        user_obj = None
        try:
            user_obj = UserModel.objects.get(username=identificador)
        except UserModel.DoesNotExist:
            # Si no existe por username, intentamos por email (case-insensitive)
            try:
                user_obj = UserModel.objects.get(email__iexact=identificador)
            except UserModel.DoesNotExist:
                user_obj = None

        # --- Caso 1: Usuario no existe ni por username ni por email ---
        if user_obj is None:
            messages.error(request, "No existe el usuario, por favor regístrese.")
            return redirect("usuario:login_estudiantes")

        # Autenticamos SIEMPRE por username interno
        user = authenticate(
            request,
            username=user_obj.username,
            password=password
        )

        # --- Caso 2: Usuario existe pero contraseña incorrecta ---
        if user is None:
            messages.error(request, "La contraseña es incorrecta.")
            return redirect("usuario:login_estudiantes")

        # --- Caso 3: Usuario existe, pero no tiene el rol adecuado ---
        if not (getattr(user, "rol", None) == "EST" or user.is_staff):
            messages.error(request, "Este usuario no tiene acceso como estudiante.")
            return redirect("usuario:login_estudiantes")

        # --- Caso 4: Usuario válido ---
        login(request, user)
        return redirect("usuario:panel_estudiante")

    # GET: mostrar formulario
    return render(request, "login/login.html")


# =====================================================
# 3. REGISTRO ESTUDIANTES (CON VALIDACIONES)
# =====================================================

def register_view(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        rut = request.POST.get("rut", "").strip()
        email = request.POST.get("email", "").strip()
        username = request.POST.get("username", "").strip()
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # 1) Validar solo letras en nombre y apellido (se permiten espacios y acentos)
        patron_nombre = r"^[A-Za-zÁÉÍÓÚÑáéíóúñ\s]+$"
        if not re.match(patron_nombre, first_name):
            messages.error(request, "El nombre solo puede contener letras.")
            return render(request, "login/register.html")

        if not re.match(patron_nombre, last_name):
            messages.error(request, "El apellido solo puede contener letras.")
            return render(request, "login/register.html")

        # 2) Validar correo institucional
        if not email.lower().endswith("@alumnos.ucn.cl"):
            messages.error(request, "El correo debe ser institucional (@alumnos.ucn.cl).")
            return render(request, "login/register.html")

        # 3) Validar RUT chileno
        if not validar_rut_chileno(rut):
            messages.error(request, "El RUT ingresado no es válido.")
            return render(request, "login/register.html")

        # 4) Validar contraseñas iguales
        if password1 != password2:
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, "login/register.html")

        # 5) Validar que el usuario no exista
        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya está en uso.")
            return render(request, "login/register.html")

        # 6) Opcional: evitar correos repetidos
        if User.objects.filter(email=email).exists():
            messages.error(request, "Ya existe un usuario con ese correo.")
            return render(request, "login/register.html")

        # 7) Validar contraseña con los validadores de Django
        dummy_user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        try:
            validate_password(password1, user=dummy_user)
        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)
            return render(request, "login/register.html")

        # 8) Crear usuario y marcarlo automáticamente como alumno
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name,
            rut=rut,
        )
        # rol alumno (EST = estudiante)
        user.rol = "EST"
        user.save()

        # Crear perfil Estudiante
        Estudiante.objects.create(usuario=user)

        messages.success(request, "Cuenta creada correctamente. Ahora puedes iniciar sesión.")
        return redirect("usuario:login_estudiantes")

    # GET
    return render(request, "login/register.html")


# =====================================================
# 2.b LOGIN DOCENTE (mismo patrón: usuario O correo)
# =====================================================

def login_docente(request):
    if request.method == "POST":
        identificador = request.POST.get("username")  # puede ser usuario O correo
        password = request.POST.get("password")

        UserModel = get_user_model()

        # 1) Buscar primero por username
        user_obj = None
        try:
            user_obj = UserModel.objects.get(username=identificador)
        except UserModel.DoesNotExist:
            # 2) Si no existe por username, buscar por email (case-insensitive)
            try:
                user_obj = UserModel.objects.get(email__iexact=identificador)
            except UserModel.DoesNotExist:
                user_obj = None

        # --- Caso 1: Usuario no existe ---
        if user_obj is None:
            messages.error(request, "No existe el usuario, por favor contacte al administrador.")
            return redirect("usuario:login_docente")

        # 3) Autenticar SIEMPRE por username interno
        user = authenticate(
            request,
            username=user_obj.username,
            password=password
        )

        # --- Caso 2: Usuario existe pero contraseña incorrecta ---
        if user is None:
            messages.error(request, "La contraseña es incorrecta.")
            return redirect("usuario:login_docente")

        # --- Caso 3: Usuario existe, pero no tiene el rol adecuado ---
        if not (
            getattr(user, "rol", None) == "DOC"  # ajusta si tu rol tiene otro código
            or user.is_staff
            or user.is_superuser
        ):
            messages.error(request, "Este usuario no tiene acceso como docente.")
            return redirect("usuario:login_docente")

        # --- Caso 4: Usuario válido ---
        login(request, user)
        # Por ahora lo mando a algún panel de docente (ajusta la url si quieres otra)
        return redirect("docente:panel")

    # GET: mostrar formulario
    return render(request, "login/login_docente.html")


# =====================================================
# 3.b REGISTRO DOCENTES (DISTINTO A ALUMNOS)
# =====================================================

def register_docente_view(request):
    if request.method == "POST":
        first_name = request.POST.get("first_name", "").strip()
        last_name = request.POST.get("last_name", "").strip()
        rut = request.POST.get("rut", "").strip()
        email = request.POST.get("email", "").strip()
        username = request.POST.get("username", "").strip()
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        # 1) Validar solo letras en nombre y apellido
        patron_nombre = r"^[A-Za-zÁÉÍÓÚÑáéíóúñ\s]+$"
        if not re.match(patron_nombre, first_name):
            messages.error(request, "El nombre solo puede contener letras.")
            return render(request, "login/register_docente.html")

        if not re.match(patron_nombre, last_name):
            messages.error(request, "El apellido solo puede contener letras.")
            return render(request, "login/register_docente.html")

        # 2) Validar correo institucional de DOCENTE
        if not email.lower().endswith("@ucn.cl"):
            messages.error(request, "El correo debe ser institucional de docente (@ucn.cl).")
            return render(request, "login/register_docente.html")

        # 3) Validar RUT chileno
        if not validar_rut_chileno(rut):
            messages.error(request, "El RUT ingresado no es válido.")
            return render(request, "login/register_docente.html")

        # 4) Validar contraseñas iguales
        if password1 != password2:
            messages.error(request, "Las contraseñas no coinciden.")
            return render(request, "login/register_docente.html")

        # 5) Validar que el usuario no exista
        if User.objects.filter(username=username).exists():
            messages.error(request, "El nombre de usuario ya está en uso.")
            return render(request, "login/register_docente.html")

        # 6) Evitar correos repetidos
        if User.objects.filter(email=email).exists():
            messages.error(request, "Ya existe un usuario con ese correo.")
            return render(request, "login/register_docente.html")

        # 7) Validar contraseña con los validadores de Django
        dummy_user = User(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
        )
        try:
            validate_password(password1, user=dummy_user)
        except ValidationError as e:
            for error in e.messages:
                messages.error(request, error)
            return render(request, "login/register_docente.html")

        # 8) Crear usuario y marcarlo como DOCENTE
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password1,
            first_name=first_name,
            last_name=last_name,
            rut=rut,
        )

        # rol lógico de docente
        user.is_staff = False      # si quieres que pueda entrar al admin, cambia a True
        user.rol = "DOC"
        user.save()

        messages.success(
            request,
            "Cuenta de docente creada correctamente. Ahora puedes iniciar sesión."
        )
        return redirect("usuario:login_docente")

    # GET
    return render(request, "login/register_docente.html")


# =====================================================
# 4. LOGOUT CON REDIRECCIÓN
# =====================================================

def redirect_to_login(request):
    es_admin = False
    if request.user.is_authenticated:
        es_admin = (
            getattr(request.user, "rol", None) == "ADM"
            or request.user.is_staff
            or request.user.is_superuser
        )

    logout(request)

    if es_admin:
        return redirect("/admin/login/")

    return redirect("usuario:login_estudiantes")


# =====================================================
# 5. RECUPERACIÓN DE CONTRASEÑA (ENVÍO DE CORREO)
# =====================================================

def forgot_password_view(request):
    """
    Pide el correo, busca el usuario y envía un enlace de recuperación.
    Luego redirige al login de estudiantes.
    """
    if request.method == "POST":
        email = request.POST.get("email", "").strip().lower()

        if not email:
            messages.error(request, "Debes ingresar un correo.")
            return render(request, "login/forgot_password.html")

        try:
            user = User.objects.get(email__iexact=email)
        except User.DoesNotExist:
            messages.error(request, "No existe una cuenta con ese correo.")
            return render(request, "login/forgot_password.html")

        # Generar UID y token
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        token = default_token_generator.make_token(user)

        # URL absoluta al enlace de restablecimiento
        reset_url = request.build_absolute_uri(
            reverse("usuario:password_reset_confirm", kwargs={"uidb64": uid, "token": token})
        )

        # Renderizar el cuerpo del correo
        context = {
            "user": user,
            "reset_url": reset_url,
        }
        subject = "Recuperación de contraseña - KinergiaRoyale"
        message = render_to_string("login/password_reset_email.txt", context)

        # Enviar correo
        send_mail(
            subject,
            message,
            getattr(settings, "DEFAULT_FROM_EMAIL", "no-reply@kinergiaroyale.local"),
            [user.email],
            fail_silently=False,
        )

        messages.success(
            request,
            "Te hemos enviado un correo con un enlace para restablecer tu contraseña."
        )
        # Redirigir al login de estudiantes
        return redirect("usuario:login_estudiantes")

    # GET
    return render(request, "login/forgot_password.html")


def password_reset_confirm(request, uidb64, token):
    """
    Vista que se abre cuando el usuario hace clic en el enlace del correo.
    Permite ingresar una nueva contraseña.
    """
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (User.DoesNotExist, ValueError, TypeError, OverflowError):
        user = None

    if user is None or not default_token_generator.check_token(user, token):
        messages.error(request, "El enlace de recuperación no es válido o ha expirado.")
        return redirect("usuario:forgot_password")

    if request.method == "POST":
        password1 = request.POST.get("password1")
        password2 = request.POST.get("password2")

        if password1 != password2:
            messages.error(request, "Las contraseñas no coinciden.")
        else:
            # Validar la contraseña con los validadores de Django
            try:
                validate_password(password1, user=user)
            except ValidationError as e:
                for error in e.messages:
                    messages.error(request, error)
            else:
                user.set_password(password1)
                user.save()
                messages.success(request, "Tu contraseña ha sido restablecida. Ahora puedes iniciar sesión.")
                return redirect("usuario:login_estudiantes")

    return render(request, "login/password_reset_confirm.html", {"uidb64": uidb64, "token": token})


# PERFIL ESTUDIANTE
@login_required
def perfil_estudiante(request):
    usuario = request.user

    # Intentamos obtener el perfil de estudiante usando el related_name='perfil'
    try:
        datos_estudiante = usuario.perfil
    except AttributeError:
        datos_estudiante = None  # Por si entra un admin o docente por error

    context = {
        "usuario": usuario,
        "estudiante": datos_estudiante
    }
    return render(request, "usuario/perfil_estudiante.html", context)
