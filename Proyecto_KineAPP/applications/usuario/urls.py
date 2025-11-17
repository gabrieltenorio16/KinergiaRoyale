from django.urls import path
from . import views

urlpatterns = [
    path("login/", views.login_estudiantes, name="login_estudiantes"),
    path("register/", views.register_view, name="register"),
    path("forgot-password/", views.forgot_password_view, name="forgot_password"),
    path("email-sent/", views.email_sent_view, name="email_sent"),
]
