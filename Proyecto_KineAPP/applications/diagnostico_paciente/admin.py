from django.contrib import admin

from .models import (
    Paciente,
    ParteCuerpo,
    CasoClinico,
    Etapa,
    TipoRespuesta,
    Respuesta,
    HistorialCurso,
    Diagnostico #NUEVODANI
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
# CASO CLÍNICO + ETAPAS inline
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
# ETAPA + RESPUESTAS inline
# ==========================
class RespuestaInline(admin.TabularInline):
    model = Respuesta
    extra = 2


@admin.register(Etapa)
class EtapaAdmin(admin.ModelAdmin):
    list_display = ('id', 'caso', 'orden', 'nombre', 'parte_cuerpo')
    list_filter = ('caso', 'parte_cuerpo')
    search_fields = ('nombre', 'caso__titulo')
    ordering = ('caso', 'orden')
    inlines = [RespuestaInline]


# ==========================
# TIPO DE RESPUESTA
# ==========================
@admin.register(TipoRespuesta)
class TipoRespuestaAdmin(admin.ModelAdmin):
    list_display = ('id', 'nombre')
    search_fields = ('nombre',)


# ==========================
# RESPUESTA
# ==========================
@admin.register(Respuesta)
class RespuestaAdmin(admin.ModelAdmin):
    list_display = ('id', 'etapa', 'tipo', 'es_correcta')
    list_filter = ('etapa', 'tipo', 'es_correcta')
    search_fields = ('contenido',)


# ==========================
# HISTORIAL DE CURSO
# ==========================
@admin.register(HistorialCurso)
class HistorialCursoAdmin(admin.ModelAdmin):
    list_display = ('id', 'curso', 'estudiante', 'fecha_inicio')
    search_fields = (
        'curso__nombre',
        'estudiante__username',
        'estudiante__first_name',
        'estudiante__last_name',
    )
    list_filter = ('curso',)
    ordering = ('-fecha_inicio',)

#############################################NUEVONUEVONUEVO(DANI)
