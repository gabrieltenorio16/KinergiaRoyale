from django.contrib import admin
from django import forms
from django.apps import apps

from .models import Contenido, Tema, Video, Pregunta, Respuesta, FichaClinica, Historial

# Obtén el modelo de usuario por label (la app está en applications/usuario)
Usuario = apps.get_model('usuario', 'usuario')


# ----- Contenido (opcional) -----
@admin.register(Contenido)
class ContenidoAdmin(admin.ModelAdmin):
    list_display = ("id", "titulo")
    search_fields = ("titulo",)


# ----- Tema -----
@admin.register(Tema)
class TemaAdmin(admin.ModelAdmin):
    list_display = ("id", "titulo", "estado_completado")
    list_filter = ("estado_completado",)
    search_fields = ("titulo", "descripcion")
    ordering = ("titulo",)


# ----- Video -----
@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("id", "titulo", "tema", "orden", "duracion")
    list_filter = ("tema",)
    search_fields = ("titulo",)
    ordering = ("tema", "orden")


# ----- Pregunta + Respuestas inline -----
class RespuestaInline(admin.TabularInline):
    model = Respuesta
    extra = 2
    fields = ("contenido", "es_correcta", "retroalimentacion")


@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    list_display = ("id", "contenido", "video", "orden")
    list_filter = ("video",)
    search_fields = ("contenido",)
    ordering = ("video", "orden")
    inlines = [RespuestaInline]


@admin.register(Respuesta)
class RespuestaAdmin(admin.ModelAdmin):
    list_display = ("id", "contenido", "pregunta", "es_correcta")
    list_filter = ("es_correcta", "pregunta__video")
    search_fields = ("contenido", "retroalimentacion")
    ordering = ("pregunta", "id")


# ----- Ficha clínica -----
@admin.register(FichaClinica)
class FichaClinicaAdmin(admin.ModelAdmin):
    list_display = ("id", "descripcion")
    search_fields = ("descripcion",)
    ordering = ("id",)


class EstudianteChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        # ID + Nombre y Apellido (puedes añadir el correo si quieres)
        return f"{obj.id} - {obj.nombre} {obj.apellido}"


class HistorialAdminForm(forms.ModelForm):
    estudiante = EstudianteChoiceField(
        queryset=Usuario.objects.filter(rol='EST'),
        label='Estudiante asociado'
    )

    class Meta:
        model = Historial
        fields = "__all__"


@admin.register(Historial)
class HistorialAdmin(admin.ModelAdmin):
    form = HistorialAdminForm
    list_display = ("id", "tema", "estudiante_id", "ficha", "fecha_registro")
    list_filter = ("tema",)
    search_fields = (
        "estudiante__id", "estudiante__nombre", "estudiante__apellido",
        "tema__titulo", "ficha__descripcion"
    )
    ordering = ("-fecha_registro",)

    # Si manejas MUCHOS usuarios y prefieres escribir el ID directamente, descomenta:
    # raw_id_fields = ("estudiante",)

    #fpknojdnsodnvsn
