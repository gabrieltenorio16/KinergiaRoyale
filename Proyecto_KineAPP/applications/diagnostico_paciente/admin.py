from django.contrib import admin

from .models import (
    Paciente,
    ParteCuerpo,
    CasoClinico,
    Etapa,
    Diagnostico,
    FichaClinicaEstudiante,
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
# ENTREVISTA (Etapa)
# ==========================
@admin.register(Etapa)
class EtapaAdmin(admin.ModelAdmin):
    list_display = ('id', 'caso', 'paciente', 'video', 'nombre')
    list_filter = ('caso__curso', 'caso', 'paciente')
    search_fields = ('nombre', 'caso__titulo', 'paciente__nombres', 'paciente__apellidos')
    ordering = ('caso', 'id')

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

# ==========================
# Ficha Clinica Estudiante
# ==========================
@admin.register(FichaClinicaEstudiante)
class FichaClinicaEstudianteAdmin(admin.ModelAdmin):
    list_display = ('id', 'curso', 'estudiante', 'paciente', 'caso_clinico', 'video', 'fecha_creacion')
    list_filter = ('caso_clinico__curso', 'fecha_creacion')
    search_fields = (
        'estudiante__username',
        'estudiante__first_name',
        'estudiante__last_name',
        'paciente__nombres',
        'paciente__apellidos',
        'caso_clinico__titulo',
    )
    ordering = ('-fecha_creacion',)

    def curso(self, obj):
        return obj.caso_clinico.curso
    curso.short_description = 'Curso'
    curso.admin_order_field = 'caso_clinico__curso__nombre'