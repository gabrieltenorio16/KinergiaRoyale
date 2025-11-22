from django.contrib import admin
from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin as DjangoUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import Docente, Estudiante

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
    


