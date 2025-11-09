from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Curso, Modulo, ContenidoAdicional

Usuario = get_user_model()

# ---- Inlines ----
class ContenidoAdicionalInline(admin.TabularInline):
    model = ContenidoAdicional
    extra = 1
    fields = ('nombre', 'directorio')

# ---- CURSO ----
@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'curso_id', 'modulos_existentes', 'cant_estudiantes')
    list_filter = ('nivel',)
    search_fields = (
        'nombre',
        'docentes__username', 'docentes__first_name', 'docentes__last_name',
        'estudiantes__username', 'estudiantes__first_name', 'estudiantes__last_name',
    )
    ordering = ('nombre',)
    readonly_fields = ('id',)
    # Mostrar selector horizontal para docentes y estudiantes (y también módulos si lo deseas)
    filter_horizontal = ('docentes', 'estudiantes', 'modulos')

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'docentes':
            kwargs['queryset'] = Usuario.objects.filter(rol='DOC')
        elif db_field.name == 'estudiantes':
            kwargs['queryset'] = Usuario.objects.filter(rol='EST')
        return super().formfield_for_manytomany(db_field, request, **kwargs)

# ---- MÓDULO ----
@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'id')
    search_fields = ('nombre',)
    ordering = ('nombre',)
    inlines = [ContenidoAdicionalInline]
    readonly_fields = ('id',)


# ---- CONTENIDO ADICIONAL ----
@admin.register(ContenidoAdicional)
class ContenidoAdicionalAdmin(admin.ModelAdmin):
    # eliminar referencias a campos eliminados (tipo_archivo, url)
    list_display = ("id", "nombre", "directorio", "modulo")
    list_filter = ("modulo",)   # usar un campo real; antes era 'tipo_archivo'
    search_fields = ("nombre",)
    ordering = ("modulo", "nombre")

