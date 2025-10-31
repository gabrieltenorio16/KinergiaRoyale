from django.apps import AppConfig

class ContenidoConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'applications.Contenido'   # <-- OJO: ruta completa, no 'diagnostico_paciente'
