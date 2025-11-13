from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError
from django.conf import settings

from .validators import validar_rut, formatear_rut


class Usuario(AbstractUser):
    ROLES = [
        ('DOC', 'Docente'),
        ('EST', 'Estudiante'),
        ('ADM', 'Administrador'),
    ]

    rut = models.CharField('RUT', max_length=20, unique=True)
    rol = models.CharField('Rol', max_length=10, choices=ROLES, default='EST')

    class Meta:
        verbose_name = "Usuario"
        verbose_name_plural = "Usuarios"
        ordering = ("first_name", "last_name")

    def clean(self):
        if self.rut:
            if not validar_rut(self.rut):
                raise ValidationError({"rut": "El RUT ingresado no es válido."})
            self.rut = formatear_rut(self.rut)

    def __str__(self):
        return f"{self.rut} - {self.first_name} {self.last_name} ({self.get_rol_display()})"


# ---------- PERFIL DOCENTE ----------
class Docente(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='perfil_docente',
        verbose_name='Usuario'
    )
    titulo = models.CharField('Título profesional', max_length=150, blank=True)
    especialidad = models.CharField('Especialidad', max_length=150, blank=True)

    class Meta:
        verbose_name = 'Docente'
        verbose_name_plural = 'Docentes'

    def __str__(self):
        return str(self.usuario)


# ---------- PERFIL ESTUDIANTE ----------
class Estudiante(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='perfil_estudiante',
        verbose_name='Usuario'
    )
    carrera = models.CharField('Carrera', max_length=150, blank=True)
    semestre = models.PositiveIntegerField('Semestre', blank=True, null=True)

    class Meta:
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'

    def __str__(self):
        return str(self.usuario)
