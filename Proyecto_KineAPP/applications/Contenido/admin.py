from django.contrib import admin
from .models import Contenido, Tema, Video, Pregunta, Respuesta, Estudiante, FichaClinica, Historial


@admin.register(Contenido)
class ContenidoAdmin(admin.ModelAdmin):
    list_display = ("id", "titulo")
    search_fields = ("titulo",)


@admin.register(Tema)
class TemaAdmin(admin.ModelAdmin):
    list_display = ("id", "titulo", "estado_completado")
    list_filter = ("estado_completado",)
    search_fields = ("titulo", "descripcion")
    ordering = ("titulo",)


@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ("id", "titulo", "tema", "orden", "duracion")
    list_filter = ("tema",)
    search_fields = ("titulo",)
    ordering = ("tema", "orden")


class RespuestaInline(admin.TabularInline):
    model = Respuesta
    extra = 2  # cantidad de filas vacías que te muestra para cargar alternativas
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


# ⬇⬇⬇ NUEVOS MODELOS: Estudiante, FichaClinica y Historial ⬇⬇⬇

@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("nombre",)
    ordering = ("nombre",)


@admin.register(FichaClinica)
class FichaClinicaAdmin(admin.ModelAdmin):
    list_display = ("id", "descripcion")
    search_fields = ("descripcion",)
    ordering = ("id",)


@admin.register(Historial)
class HistorialAdmin(admin.ModelAdmin):
    list_display = ("id", "estudiante", "tema", "ficha", "fecha_registro")
    list_filter = ("tema", "estudiante")
    search_fields = ("estudiante__nombre", "tema__titulo", "ficha__descripcion")
    ordering = ("-fecha_registro",)
