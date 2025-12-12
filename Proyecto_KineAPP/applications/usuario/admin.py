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
#@admin.register(Docente)
#class DocenteAdmin(admin.ModelAdmin):
#    list_display = ('id', 'usuario', 'titulo', 'especialidad')
#    search_fields = (
#        'usuario__username', 'usuario__first_name', 'usuario__last_name', 'usuario__rut',
#    )
#    autocomplete_fields = ('usuario',)


#---------- ESTUDIANTE (Mejorado) ----------
#@admin.register(Estudiante)
#class EstudianteAdmin(admin.ModelAdmin):
#    list_display = ('id', 'usuario', 'carrera', 'semestre')
#    search_fields = (
#        'usuario__username', 'usuario__first_name', 'usuario__last_name', 'usuario__rut', 'carrera',
#    )
#    list_filter = ('carrera', 'semestre')
#    autocomplete_fields = ('usuario',)
    
# ---------- DASHBOARD GENERAL (Modelo proxy para mostrar botón en sidebar) ----------
from django.shortcuts import redirect
from django.utils.html import format_html
from .models import DashboardGeneralProxy


@admin.register(DashboardGeneralProxy)
class DashboardGeneralAdmin(admin.ModelAdmin):

    # Redirige automáticamente al Dashboard General
    def changelist_view(self, request, extra_context=None):
        return redirect("/usuario/admin/dashboard/")

    # Muestra un botón dentro de la vista (no afecta al sidebar)
    list_display = ("ir_al_dashboard",)

    def ir_al_dashboard(self, obj=None):
        return format_html(
            '<a class="button" href="/usuario/admin/dashboard/">Ir al Dashboard General</a>'
        )

    ir_al_dashboard.short_description = "Dashboard General"


