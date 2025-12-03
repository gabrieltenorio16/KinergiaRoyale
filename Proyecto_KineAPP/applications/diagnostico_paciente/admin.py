from django.contrib import admin

from .models import (
    Paciente,
    ParteCuerpo,
    CasoClinico,
    Etapa,
    Diagnostico,
)


# ==========================
# PACIENTE
# ==========================
@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    list_display = ('id', 'apellidos', 'nombres', 'edad')
    search_fields = ('nombres', 'apellidos')
    ordering = ('apellidos', 'nombres')


# ==========================
# PARTE DEL CUERPO
# ==========================
@admin.register(ParteCuerpo)
class ParteCuerpoAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)


# ==========================
# CASO CLINICO + ETAPAS inline
# ==========================
class EtapaInline(admin.TabularInline):
    model = Etapa
    extra = 1


@admin.register(CasoClinico)
class CasoClinicoAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'paciente', 'curso', 'fecha_creacion')
    list_filter = ('curso',)
    search_fields = ('titulo', 'paciente__nombres', 'paciente__apellidos')
    ordering = ('-fecha_creacion',)
    inlines = [EtapaInline]


# ==========================
# ETAPA
# ==========================
@admin.register(Etapa)
class EtapaAdmin(admin.ModelAdmin):
    list_display = ('id', 'caso', 'nombre', 'parte_cuerpo')
    list_filter = ('caso', 'parte_cuerpo')
    search_fields = ('nombre', 'caso__titulo')
    ordering = ('caso', 'nombre')

    # esto hace que aparezca el widget de dos listas con filtro,
    # para elegir las preguntas disponibles para la etapa
    filter_horizontal = ('preguntas',)


# ==========================
# DIAGNOSTICO
# ==========================
@admin.register(Diagnostico)
class DiagnosticoAdmin(admin.ModelAdmin):
    list_display = ('id', 'paciente', 'parte_cuerpo')
    list_filter = ('parte_cuerpo',)
    search_fields = (
        'paciente__nombres',
        'paciente__apellidos',
        'parte_cuerpo__nombre',
    )


