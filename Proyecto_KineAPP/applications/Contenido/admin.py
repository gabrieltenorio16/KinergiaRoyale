from django.contrib import admin
from .models import Contenido  # <-- IMPORTA el modelo

@admin.register(Contenido)
class ContenidoAdmin(admin.ModelAdmin):
    list_display = ("id", "titulo")
    search_fields = ("titulo",)
