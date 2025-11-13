from django.db import models
from django.conf import settings  # Referencia a AUTH_USER_MODEL


# -----------------------------
# CURSO
# -----------------------------
class Curso(models.Model):
    NIVEL_CHOICES = [
        ('BASICO', 'Básico'),
        ('INTERMEDIO', 'Intermedio'),
        ('AVANZADO', 'Avanzado'),
    ]

    nombre = models.CharField('Nombre del curso', max_length=100)
    nivel = models.CharField('Nivel', max_length=10, choices=NIVEL_CHOICES, default='BASICO')

    # Un curso puede tener varios docentes (un paralelo con varios profesores)
    docentes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='cursos_como_docente',
        blank=True,
        verbose_name='Docentes',
    )

    # Un curso puede tener varios estudiantes
    estudiantes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='cursos_como_estudiante',
        blank=True,
        verbose_name='Estudiantes',
    )

    class Meta:
        verbose_name = 'Curso'
        verbose_name_plural = 'Cursos'
        ordering = ('nombre',)

    def __str__(self):
        return f"{self.nombre} ({self.get_nivel_display()})"

    # Métodos auxiliares para Admin
    def cant_docentes(self):
        return self.docentes.count()
    cant_docentes.short_description = "N° Docentes"

    def cant_estudiantes(self):
        return self.estudiantes.count()
    cant_estudiantes.short_description = "N° Estudiantes"
