from django.urls import path
from . import views

app_name = "usuario"

print(">>> CARGANDO URLS DE USUARIO <<<")

urlpatterns = [
    # Autenticación
    path("login/", views.login_estudiantes, name="login_estudiantes"),
    path("logout/", views.redirect_to_login, name="logout"),

    # Recuperación / registro
    path("registro/", views.register_view, name="register_view"),
    path("forgot-password/", views.forgot_password_view, name="forgot_password"),

    # Panel de usuario
    path("panel/", views.panel_estudiante, name="panel_estudiante"),

    # Panel de estadísticas del administrador
    path("admin/dashboard/", views.admin_dashboard, name="admin_dashboard"),
]
