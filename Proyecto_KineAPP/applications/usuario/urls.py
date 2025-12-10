from django.urls import path
from . import views

app_name = "usuario"

urlpatterns = [
    # Selección de tipo de entrada
    path("", views.seleccionar_entrada, name="seleccionar_entrada"),
    path("staff/", views.seleccionar_staff, name="seleccionar_staff"),

    # Logins
    path("login/", views.login_estudiantes, name="login_estudiantes"),
    path("login-docente/", views.login_docente, name="login_docente"),

    # Logout
    path("logout/", views.redirect_to_login, name="logout"),

    # Registro y recuperación
    path("registro/", views.register_view, name="register_view"),  # alumnos
    path("registro-docente/", views.register_docente_view, name="register_docente_view"),
    path("forgot-password/", views.forgot_password_view, name="forgot_password"),
    path(
        "reset-password/<uidb64>/<token>/",
        views.password_reset_confirm,
        name="password_reset_confirm",
    ),

    # Paneles estudiante
    path("panel/", views.panel_estudiante, name="panel_estudiante"),          # INICIO
    path("cursos/", views.cursos_estudiante, name="cursos_estudiante"),       # CURSOS
    path("casos/", views.casos_estudiante, name="casos_estudiante"),          # CASOS CLÍNICOS

    # Perfil Estudiante
    path("perfil/", views.perfil_estudiante, name="perfil"),
]
