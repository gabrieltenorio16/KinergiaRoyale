from django.contrib import admin
from django.urls import path, include
from applications.usuario.views import redirect_to_login

urlpatterns = [
    path("", redirect_to_login, name="root_redirect"),

    path("admin/", admin.site.urls),

    # Usuarios
    path("usuario/", include("applications.usuario.urls")),

    # Cursos y videos (tu app nueva)
    path("videos/", include("applications.curso_y_modulo.urls")),

    # Diagnóstico (app antigua o de tu compañera)
    path("simulacion/", include("applications.diagnostico_paciente.urls")),
]
