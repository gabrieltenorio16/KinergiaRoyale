from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect  # 👈 usamos redirect en la raíz

print(">>> REGISTRANDO INCLUDE usuario <<<")

urlpatterns = [
    # Raíz del sitio -> pantalla "¿Cómo quieres entrar?"
    path(
        "",
        lambda request: redirect("usuario:seleccionar_entrada"),
        name="root_redirect"
    ),

    path("admin/", admin.site.urls),

    # Usuarios
    path("usuario/", include("applications.usuario.urls")),

    # Cursos y videos
    path("videos/", include("applications.curso_y_modulo.urls")),

    # Diagnóstico
    path("simulacion/", include("applications.diagnostico_paciente.urls")),

    # Contenido
    path("contenido/", include("applications.Contenido.urls")),
]
