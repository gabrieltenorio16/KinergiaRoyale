from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from .validators import validar_rut, formatear_rut


class Usuario(AbstractUser):
    Roles = [
        ('DOC', 'Docente'),
        ('EST', 'Estudiante'),
        ('ADM', 'Administrador'),
    ]

    rut = models.CharField('RUT', max_length=20, unique=True)
    rol = models.CharField('Rol', max_length=10, choices=Roles, default='EST')

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ("first_name", "last_name")  # ← Cambiado

    def clean(self):
        if self.rut:
            if not validar_rut(self.rut):
                raise ValidationError({"rut": "El RUT ingresado no es válido."})
            self.rut = formatear_rut(self.rut)

    def __str__(self):
        return f"{self.rut} - {self.first_name} {self.last_name} ({self.get_rol_display()})"
