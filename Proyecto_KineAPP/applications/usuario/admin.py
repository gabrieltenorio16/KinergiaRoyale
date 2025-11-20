from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

# IMPORTANTE: Asegúrate de importar Modulo aquí
from .models import Docente, Estudiante, Modulo 

Usuario = get_user_model()

@admin.register(Usuario)
class UsuarioAdmin(DjangoUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email', 'rut')}),
        (_('Permissions'), {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
        (_('Rol'), {'fields': ('rol',)}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'rut', 'rol', 'password1', 'password2'),
        }),
    )
    list_display = ('username', 'first_name', 'last_name', 'email', 'rut', 'rol', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'rut')
    ordering = ('username',)

    class Media:
        js = ("js/mask_rut.js",)


# ---------- DOCENTE ----------
@admin.register(Docente)
class DocenteAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'titulo', 'especialidad')
    search_fields = (
        'usuario__username', 'usuario__first_name', 'usuario__last_name', 'usuario__rut',
    )
    autocomplete_fields = ('usuario',)


# ---------- ESTUDIANTE (Mejorado) ----------
@admin.register(Estudiante)
class EstudianteAdmin(admin.ModelAdmin):
    list_display = ('id', 'usuario', 'carrera', 'semestre')
    search_fields = (
        'usuario__username', 'usuario__first_name', 'usuario__last_name', 'usuario__rut', 'carrera',
    )
    list_filter = ('carrera', 'semestre')
    autocomplete_fields = ('usuario',)
    
    # ESTO ES CRÍTICO: Permite seleccionar múltiples módulos fácilmente
    # Requiere que en models.py Estudiante tenga: modulos = models.ManyToManyField(Modulo)
    filter_horizontal = ('modulos',) 


# ---------- MODULO (NUEVO) ----------
@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion_corta') # Ajusta según tus campos
    search_fields = ('nombre',)
    
    # Truco para mostrar descripción corta en la lista
    def descripcion_corta(self, obj):
        return obj.descripcion[:50] + '...' if obj.descripcion else '-'
