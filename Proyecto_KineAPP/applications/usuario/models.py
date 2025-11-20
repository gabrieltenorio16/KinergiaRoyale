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
    rut = models.CharField('RUT', max_length=12, unique=True)
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
        nombre = f"{self.first_name} {self.last_name}".strip() or self.username
        return f"{nombre} ({self.get_rol_display()})"


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


# ======================================================
# 1. AQUÍ ESTÁ LA CLAVE: EL MODELO MODULO QUE FALTABA
# ======================================================
class Modulo(models.Model):
    nombre = models.CharField('Nombre del Módulo', max_length=100)
    descripcion = models.TextField('Descripción', blank=True, null=True)

    class Meta:
        verbose_name = 'Módulo'
        verbose_name_plural = 'Módulos'

    def __str__(self):
        return self.nombre


# ---------- PERFIL ESTUDIANTE ----------
class Estudiante(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='perfil',  # Ojo: related_name='perfil' para que funcione el login
        verbose_name='Usuario'
    )
    carrera = models.CharField('Carrera', max_length=150, blank=True)
    semestre = models.PositiveIntegerField('Semestre', blank=True, null=True)

    # CONEXIÓN CON MÓDULOS
    modulos = models.ManyToManyField(
        Modulo, 
        blank=True, 
        related_name='estudiantes',
        verbose_name='Módulos Inscritos'
    )

    class Meta:
        verbose_name = 'Estudiante'
        verbose_name_plural = 'Estudiantes'

    def __str__(self):
        return str(self.usuario)