from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Curso, SeleccionPacienteCurso

Usuario = get_user_model()


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    list_display = (
        'nombre',
        'curso_id',
        'nivel',
        'fecha_inicio',
        'fecha_fin',
        'cant_docentes',
        'cant_estudiantes',
    )
    list_filter = ('nivel',)
    search_fields = (
        'nombre',
        'docentes__username', 'docentes__first_name', 'docentes__last_name',
        'estudiantes__username', 'estudiantes__first_name', 'estudiantes__last_name',
    )
    ordering = ('nombre',)
    readonly_fields = ('id',)
    filter_horizontal = ('docentes', 'estudiantes')

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        if db_field.name == 'docentes':
            kwargs['queryset'] = Usuario.objects.filter(rol='DOC')
        elif db_field.name == 'estudiantes':
            kwargs['queryset'] = Usuario.objects.filter(rol='EST')
        return super().formfield_for_manytomany(db_field, request, **kwargs)

    def curso_id(self, obj):
        return obj.id
    curso_id.short_description = 'ID'
    curso_id.admin_order_field = 'id'


#@admin.register(SeleccionPacienteCurso)
#class SeleccionPacienteCursoAdmin(admin.ModelAdmin):
#    list_display = ('usuario', 'curso', 'paciente', 'fecha_seleccion')
#    list_filter = ('curso', 'fecha_seleccion')
#    search_fields = (
#        'usuario__username',
#        'usuario__first_name',
#        'usuario__last_name',
#        'curso__nombre',
#        'paciente__nombres',
#        'paciente__apellidos',
#    )
#    ordering = ('-fecha_seleccion',)
