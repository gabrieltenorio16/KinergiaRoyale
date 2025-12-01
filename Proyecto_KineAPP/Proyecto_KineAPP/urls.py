from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path("", lambda request: redirect("usuario:seleccionar_entrada"), name="root_redirect"),

    path("admin/", admin.site.urls),

    path("usuario/", include("applications.usuario.urls")),
    path("contenido/", include("applications.Contenido.urls")),

    # 👇 Aquí ya puedes usar namespace porque curso.py tiene app_name = "curso"
    path(
        "curso/",
        include("applications.curso_y_modulo.urls.curso", namespace="curso"),
    ),
    path(
        "simulacion/",
        include("applications.curso_y_modulo.urls.simulacion", namespace="simulacion"),
    ),
    path(
        "docente/",
        include("applications.curso_y_modulo.urls.docente", namespace="docente"),
    ),
]
