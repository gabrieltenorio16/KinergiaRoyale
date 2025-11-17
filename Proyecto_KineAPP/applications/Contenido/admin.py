from django.contrib import admin
from django import forms
from django.contrib.auth import get_user_model

from .models import Tema, Video, Pregunta, Buscador_de_respuesta, FichaClinica, Historial

#Usuario = get_user_model()


# ----- Tema -----
@admin.register(Tema)
class TemaAdmin(admin.ModelAdmin):
    list_display = ("id", "titulo")


#----- Video -----
@admin.register(Video)
class VideoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'tema', 'url', 'id')
    list_filter = ('tema',)
    ordering = ('tema', 'id')
    search_fields = ('titulo', 'tema__titulo')


# ----- Pregunta + Respuestas inline -----
#class RespuestaInline(admin.TabularInline):
#    model = Buscador_de_respuesta
 #   extra = 2
  #  fields = ("contenido", "es_correcta", "retroalimentacion")


#@admin.register(Pregunta)
#class PreguntaAdmin(admin.ModelAdmin):
 #   list_display = ("id", "contenido_corto", "video", "orden")
  #  list_filter = ("video",)
   # search_fields = ("contenido", "video__titulo")
   # ordering = ("video", "orden")
    #inlines = [RespuestaInline]

    #def contenido_corto(self, obj):
     #   return (obj.contenido[:60] + '...') if len(obj.contenido) > 60 else obj.contenido
    #contenido_corto.short_description = "Pregunta"


#@admin.register(Buscador_de_respuesta)
#class BuscadorDeRespuestaAdmin(admin.ModelAdmin):
 #   list_display = ('id', 'pregunta_display', 'contenido_corto', 'es_correcta')
  #  search_fields = ('contenido', 'pregunta__contenido', 'pregunta__video__titulo')
   # list_filter = ('es_correcta', 'pregunta__video')

#    def pregunta_display(self, obj):
 #       return str(obj.pregunta) if obj.pregunta else ''
  #  pregunta_display.short_description = 'Pregunta'

#    def contenido_corto(self, obj):
 #       return (obj.contenido[:60] + '...') if len(obj.contenido) > 60 else obj.contenido
  #  contenido_corto.short_description = "Respuesta"

   # def es_correcta(self, obj):
    #    return getattr(obj, 'es_correcta', False)
    #es_correcta.short_description = 'Es correcta'
    #es_correcta.boolean = True


# ----- Ficha clínica -----
@admin.register(FichaClinica)
class FichaClinicaAdmin(admin.ModelAdmin):
    list_display = ("id", "caso_clinico", "descripcion_corta")
    search_fields = ("descripcion", "caso_clinico__titulo")
    ordering = ("id",)

    def descripcion_corta(self, obj):
        if not obj.descripcion:
            return ""
        return (obj.descripcion[:60] + '...') if len(obj.descripcion) > 60 else obj.descripcion
    descripcion_corta.short_description = "Descripción"


# ----- Historial -----

#class EstudianteChoiceField(forms.ModelChoiceField):
 #   def label_from_instance(self, obj):
  ##         texto = str(obj).strip()
    #        if texto:
     #           return texto
      #  except Exception:
       #     pass

#        first = getattr(obj, 'first_name', '') or ''
 ##      if first or last:
   #         return f"{obj.id} - {first} {last}".strip()
#
 #       return getattr(obj, 'username', f'Usuario {getattr(obj, "id", "?")}')


#class HistorialAdminForm(forms.ModelForm):
 #   estudiante = EstudianteChoiceField(
  #      queryset=Usuario.objects.filter(rol='EST'),
   #     label='Estudiante asociado'
 #   )

  #  class Meta:
   #     model = Historial
    #    fields = "__all__"


#@admin.register(Historial)
#class HistorialAdmin(admin.ModelAdmin):
 #   form = HistorialAdminForm
  #  list_display = ("id", "tema", "estudiante", "ficha", "fecha_registro")
   # list_filter = ("tema", "tema__modulo")
    #search_fields = (
     #   "estudiante__id", "estudiante__username", "estudiante__first_name", "estudiante__last_name",
      #  "tema__titulo", "tema__modulo__nombre", "ficha__descripcion"
   # )
   # ordering = ("-fecha_registro",)
