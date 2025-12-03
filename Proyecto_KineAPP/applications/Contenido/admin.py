from django.contrib import admin

from .models import Tema, Video, Topico, Pregunta, Respuesta


# ----- Tema -----
@admin.register(Tema)
class TemaAdmin(admin.ModelAdmin):
    list_display = ("id", "titulo")
    search_fields = ("titulo",)


# ----- Video -----
@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tema', 'url', 'id')
    list_filter = ('tema',)
    ordering = ('tema', 'id')
    search_fields = ('titulo', 'tema__titulo')


# ----- Tópico -----
@admin.register(Topico)
class TopicoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre")
    search_fields = ("nombre",)


# ----- Pregunta -----
@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    list_display = ("id", "pregunta", "topico")
    search_fields = ("pregunta", "topico__nombre")
    list_filter = ("topico",)


# ----- Respuesta -----
@admin.register(Respuesta)
class RespuestaAdmin(admin.ModelAdmin):
    list_display = ("id", "pregunta", "es_correcta")
    list_filter = ("es_correcta", "pregunta__topico")
    search_fields = ("contenido", "pregunta__pregunta")
