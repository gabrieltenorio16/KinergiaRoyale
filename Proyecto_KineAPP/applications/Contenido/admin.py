from django.contrib import admin
from django import forms
from django.contrib.auth import get_user_model

from .models import Tema, Video, Pregunta, Buscador_de_respuesta, FichaClinica, Historial

# Obtén el modelo de usuario por label (la app está en applications/usuario)
# Antes: Usuario = apps.get_model('usuario', 'usuario')
Usuario = get_user_model()


# ----- Contenido (opcional) -----
#@admin.register(Contenido)
#class ContenidoAdmin(admin.ModelAdmin):
    #list_display = ('titulo',)
    #search_fields = ("titulo",)


# ----- Tema -----
@admin.register(Tema)
class TemaAdmin(admin.ModelAdmin):
    list_display = ('id', 'titulo', 'estado_completado')
    list_editable = ('estado_completado',)
    list_filter = ('estado_completado',)
    search_fields = ('titulo', 'descripcion')
    ordering = ('titulo',)


# ----- Video -----
@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tema', 'url', 'id')
    ordering = ('tema', 'id')


# ----- Pregunta + Respuestas inline -----
class RespuestaInline(admin.TabularInline):
    model = Buscador_de_respuesta
    extra = 2
    fields = ("contenido", "es_correcta", "retroalimentacion")


@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    list_display = ("id", "contenido", "video")
    list_filter = ("video",)
    search_fields = ("contenido",)
    ordering = ("video",)
    inlines = [RespuestaInline]


@admin.register(Buscador_de_respuesta)  # o reemplaza por `Respuesta` si ese es el nombre en tu proyecto
class BuscadorDeRespuestaAdmin(admin.ModelAdmin):
    # Mostrar campos directos y con etiquetas claras
    list_display = ('id', 'pregunta_display', 'contenido', 'es_correcta')
    search_fields = ('contenido', 'pregunta__contenido')

    def pregunta_display(self, obj):
        return str(obj.pregunta) if obj.pregunta else ''
    pregunta_display.short_description = 'Pregunta'

    def es_correcta(self, obj):
        return getattr(obj, 'es_correcta', False)
    es_correcta.short_description = 'Es correcta'
    es_correcta.boolean = True


# ----- Ficha clínica -----
@admin.register(FichaClinica)
class FichaClinicaAdmin(admin.ModelAdmin):
    list_display = ("id", "descripcion")
    search_fields = ("descripcion",)
    ordering = ("id",)


class EstudianteChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        # Evita acceder a atributos que no existen (nombre/apellido).
        # Prioriza: __str__ definido en tu modelo -> first_name/last_name -> username -> id.
        try:
            texto = str(obj).strip()
            if texto:
                return texto
        except Exception:
            pass

        first = getattr(obj, 'first_name', '') or ''
        last = getattr(obj, 'last_name', '') or ''
        if first or last:
            return f"{obj.id} - {first} {last}".strip()

        return getattr(obj, 'username', f'Usuario {getattr(obj, "id", "?")}')


class HistorialAdminForm(forms.ModelForm):
    # Nota: se asume que Usuario existe en apps.get_model; si no, revisar app_label/model_name
    estudiante = EstudianteChoiceField(
        queryset=Usuario.objects.filter(rol='EST'),
        label='Estudiante asociado'
    )

    class Meta:
        model = Historial
        fields = "__all__"


@admin.register(Historial)
class HistorialAdmin(admin.ModelAdmin):
    form = HistorialAdminForm
    # Mostrar el objeto estudiante (usa __str__ del modelo Usuario)
    list_display = ("id", "tema", "estudiante", "ficha", "fecha_registro")
    list_filter = ("tema",)
    search_fields = (
        "estudiante__id", "estudiante__username", "estudiante__first_name", "estudiante__last_name",
        "tema__titulo", "ficha__descripcion"
    )
    ordering = ("-fecha_registro",)

    # Si manejas MUCHOS usuarios y prefieres escribir el ID directamente, descomenta:
    # raw_id_fields = ("estudiante",)

    #fpknojdnsodnvsn


class UsuarioModelChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        # Preferir __str__ (tu Usuario.__str__ está definido),
        # luego get_full_name(), luego username, luego id.
        try:
            texto = str(obj).strip()
            if texto:
                return texto
        except Exception:
            pass

        if hasattr(obj, 'get_full_name'):
            full = obj.get_full_name()
            if full:
                return full

        return getattr(obj, 'username', f'Usuario {getattr(obj, "id", "?")}')
