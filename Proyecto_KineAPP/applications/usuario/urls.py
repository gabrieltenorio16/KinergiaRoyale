from django.urls import path
from . import views

app_name = 'usuario' 

urlpatterns = [
    # Login (coincide con 'usuario:login_estudiantes' si lo usaras, o redirige aquí)
    path('login/', views.login_estudiantes, name='login_estudiantes'),
    
    # Registro (ESTA ES LA QUE FALLABA, le puse name='register_view')
    path('registro/', views.register_view, name='register_view'),
    
    # Panel
    path('panel/', views.panel_estudiante, name='panel_estudiante'),
    
    # Recuperar contraseña (name='forgot_password')
    path('forgot-password/', views.forgot_password_view, name='forgot_password'),
    
    # Logout
    path('logout/', views.redirect_to_login, name='logout'),
]