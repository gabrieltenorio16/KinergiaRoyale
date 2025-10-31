from django.contrib import admin
from .models import Curso, Modulo, Docente, ContenidoAdicional 
# Asegúrate de que todos estos modelos existan y estén importados correctamente

# --- 1. Definición de Inlines (Para gestionar relaciones) ---

# Muestra el Contenido Adicional DENTRO de la página de edición del Módulo.
class ContenidoAdicionalInline(admin.TabularInline):
    model = ContenidoAdicional
    extra = 1
    fields = ('nombre', 'tipo_archivo', 'url', 'directorio')
    # Opcional: Si el campo 'modulo' es null=True, añade 'can_delete = False'
    # o 'raw_id_fields = ("modulo",)' para mejorar la búsqueda.
    
# Muestra los Módulos DENTRO de la página de edición del Curso.
class ModuloInline(admin.TabularInline):
    model = Modulo
    extra = 1
    fields = ('nombre',)


# --- 2. Clases ModelAdmin con Decorador (@admin.register) ---

@admin.register(Docente)
class DocenteAdmin(admin.ModelAdmin):
    # El campo 'nombre' está disponible directamente.
    list_display = ('nombre', 'id') 
    search_fields = ('nombre',)
    readonly_fields = ('id',)


@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    # Muestra el nombre del Curso, el Docente y el Nivel legible.
    list_display = ('nombre', 'docente', 'get_nivel_display', 'id')
    
    list_filter = ('nivel', 'docente')
    # Permite buscar por nombre del curso y nombre del Docente.
    search_fields = ('nombre', 'docente__nombre')
    ordering = ('nombre',)

@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'curso', 'id')
    list_filter = ('curso',)
    search_fields = ('nombre', 'curso__nombre')
    ordering = ('curso', 'nombre')
    
    # Incluye el Contenido Adicional en la página de edición del Módulo.
    inlines = [ContenidoAdicionalInline]
    readonly_fields = ('id',)


@admin.register(ContenidoAdicional)
class ContenidoAdicionalAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'tipo_archivo', 'modulo', 'id')
    list_filter = ('tipo_archivo', 'modulo')
    search_fields = ('nombre', 'modulo__nombre')
    readonly_fields = ('id',)
    ordering = ('modulo', 'nombre')