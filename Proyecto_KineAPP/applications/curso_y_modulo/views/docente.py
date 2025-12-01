from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth import get_user_model

from applications.curso_y_modulo.models import Curso

User = get_user_model()


# =====================================================
# PANEL MAESTRO – CLASES
# =====================================================
@login_required
def panel_maestro_docente(request):

    if request.user.rol != "DOC":
        messages.error(request, "No tienes permisos para acceder al panel docente.")
        return redirect("root_redirect")

    usuario = request.user
    cursos = Curso.objects.filter(docentes=usuario).prefetch_related("docentes", "estudiantes")

    estudiantes = User.objects.filter(rol="EST").order_by("first_name", "last_name")
    docentes = User.objects.filter(rol="DOC").order_by("first_name", "last_name")

    return render(request, "docente/panel_maestro.html", {
        "cursos": cursos,
        "estudiantes": estudiantes,
        "docentes": docentes,
        "tab": "clases",
    })


# =====================================================
# TAB: ESTUDIANTES
# =====================================================
@login_required
def panel_maestro_estudiantes(request):

    if request.user.rol != "DOC":
        messages.error(request, "No tienes permisos.")
        return redirect("root_redirect")

    estudiantes = User.objects.filter(rol="EST").order_by("first_name", "last_name")

    return render(request, "docente/panel_maestro_estudiantes.html", {
        "estudiantes": estudiantes,
        "tab": "estudiantes",
    })


# =====================================================
# TAB: RECURSOS
# =====================================================
@login_required
def panel_maestro_recursos(request):

    if request.user.rol != "DOC":
        messages.error(request, "No tienes permisos.")
        return redirect("root_redirect")

    return render(request, "docente/panel_maestro_recursos.html", {
        "tab": "recursos",
    })


# =====================================================
# ACCIÓN: CREAR CURSO
# =====================================================
@login_required
@require_POST
def crear_curso_view(request):

    if request.user.rol != "DOC":
        messages.error(request, "No tienes permisos.")
        return redirect("root_redirect")

    nombre = request.POST.get("nombre")
    nivel = request.POST.get("nivel")
    fecha_inicio = request.POST.get("fecha_inicio") or None
    fecha_fin = request.POST.get("fecha_fin") or None

    docentes_ids = request.POST.getlist("docentes_ids")
    estudiantes_ids = request.POST.getlist("estudiantes_ids")

    if not nombre:
        messages.error(request, "El nombre del curso es obligatorio.")
        return redirect("docente:panel")

    curso = Curso.objects.create(
        nombre=nombre,
        nivel=nivel,
        fecha_inicio=fecha_inicio,
        fecha_fin=fecha_fin,
    )

    docentes = User.objects.filter(id__in=docentes_ids, rol="DOC")
    estudiantes = User.objects.filter(id__in=estudiantes_ids, rol="EST")

    curso.docentes.add(*docentes)
    curso.estudiantes.add(*estudiantes)

    messages.success(request, f"Curso '{curso.nombre}' creado correctamente.")
    return redirect("docente:panel")


# =====================================================
# ACCIÓN: AGREGAR/QIUTAR ESTUDIANTES
# =====================================================
@login_required
@require_POST
def agregar_estudiantes_view(request, curso_id):

    if request.user.rol != "DOC":
        messages.error(request, "No tienes permisos.")
        return redirect("root_redirect")

    curso = get_object_or_404(Curso, id=curso_id)
    estudiantes_ids = request.POST.getlist("estudiantes_ids")
    accion = request.POST.get("accion")

    estudiantes = User.objects.filter(id__in=estudiantes_ids, rol="EST")

    if accion == "quitar":
        curso.estudiantes.remove(*estudiantes)
        messages.success(request, "Estudiantes eliminados.")
    else:
        curso.estudiantes.add(*estudiantes)
        messages.success(request, "Estudiantes agregados.")

    return redirect("docente:panel")
# =====================================================


