from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Curso, Modulo, ContenidoAdicional

User = get_user_model()


# ---- Inlines ----
class ContenidoAdicionalInline(admin.TabularInline):
    model = ContenidoAdicional
    extra = 1
    fields = ('nombre', 'tipo_archivo', 'url', 'directorio')


class ModuloInline(admin.TabularInline):
    model = Modulo
    extra = 1
    fields = ('nombre',)


# ---- Curso ----
@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'get_nivel_display', 'cant_docentes', 'cant_estudiantes', 'id')
    list_filter = ('nivel',)
    search_fields = (
        'nombre',
        'docentes__username', 'docentes__first_name', 'docentes__last_name',
        'estudiantes__username', 'estudiantes__first_name', 'estudiantes__last_name',
    )
    ordering = ('nombre',)
    inlines = [ModuloInline]
    readonly_fields = ('id',)

    # Selector múltiple cómodo
    filter_horizontal = ('docentes', 'estudiantes')

    # Filtra por rol (ajusta si usas grupos)
    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'docentes':
            kwargs['queryset'] = User.objects.filter(rol='DOCENTE')
            # kwargs['queryset'] = User.objects.filter(groups__name='Docentes')  # <-- si usas grupos
        elif db_field.name == 'estudiantes':
            kwargs['queryset'] = User.objects.filter(rol='ESTUDIANTE')
            # kwargs['queryset'] = User.objects.filter(groups__name='Estudiantes')  # <-- si usas grupos
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def cant_docentes(self, obj):
        return obj.docentes.count()
    cant_docentes.short_description = 'Docentes'

    def cant_estudiantes(self, obj):
        return obj.estudiantes.count()
    cant_estudiantes.short_description = 'Estudiantes'


# ---- Módulo ----
@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'curso', 'id')
    list_filter = ('curso',)
    search_fields = ('nombre', 'curso__nombre')
    ordering = ('curso', 'nombre')
    inlines = [ContenidoAdicionalInline]
    readonly_fields = ('id',)


# ---- Contenido Adicional ----
@admin.register(ContenidoAdicional)
class ContenidoAdicionalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo_archivo', 'modulo', 'id')
    list_filter = ('tipo_archivo', 'modulo')
    search_fields = ('nombre', 'modulo__nombre')
    readonly_fields = ('id',)
    ordering = ('modulo', 'nombre')

