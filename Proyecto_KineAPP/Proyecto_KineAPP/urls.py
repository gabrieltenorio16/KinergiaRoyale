from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect  # 👈 usamos redirect en la raíz

print(">>> REGISTRANDO INCLUDE usuario <<<")

urlpatterns = [
    path("", lambda request: redirect("usuario:seleccionar_entrada"), name="root_redirect"),

    path("admin/", admin.site.urls),

    path("usuario/", include("applications.usuario.urls")),
    path("contenido/", include("applications.Contenido.urls")),

    # Sección estudiante
    path("curso/", include("applications.curso_y_modulo.urls.curso")),

    # Sección simulación
    path("simulacion/", include("applications.curso_y_modulo.urls.simulacion")),

    # Sección docente
    path("docente/", include("applications.curso_y_modulo.urls.docente")),
]
