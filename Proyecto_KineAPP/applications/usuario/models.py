from django.contrib.auth.models import AbstractUser
from django.db import models


class Usuario(AbstractUser):
    username = models.CharField(max_length=150, unique=True, null=True, blank=True)

    Roles = [
        ('DOC', 'Docente'),
        ('EST', 'Estudiante'),
        ('ADM', 'Administrador'),
    ]

    rut = models.CharField('RUT', max_length=20, unique=True, null=True, blank=True)
    rol = models.CharField('Rol', max_length=10, choices=Roles, default='EST')

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ('username',)

    def __str__(self):
        return f"{self.username} - {self.get_rol_display()}"
