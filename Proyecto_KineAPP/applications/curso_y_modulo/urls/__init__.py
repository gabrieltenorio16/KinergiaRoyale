# applications/curso_y_modulo/urls/__init__.py

from .curso import urlpatterns as curso_urlpatterns
from .simulacion import urlpatterns as simulacion_urlpatterns
from .docente import urlpatterns as docente_urlpatterns

# Namespace de la app (lo usamos como 'curso_y_modulo' en los templates)
app_name = "curso_y_modulo"

# Unimos todas las rutas de los 3 módulos
urlpatterns = (
    curso_urlpatterns
    + simulacion_urlpatterns
    + docente_urlpatterns
)
