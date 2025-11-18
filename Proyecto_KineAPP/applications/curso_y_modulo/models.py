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

    # NUEVO: Fechas solicitadas en los requerimientos
    fecha_inicio = models.DateField(
        'Fecha de inicio del curso',
        null=True,
        blank=True
    )
    fecha_fin = models.DateField(
        'Fecha de fin del curso',
        null=True,
        blank=True
    )

    # Un curso puede tener varios docentes
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


# -----------------------------
# SELECCIÓN DE PACIENTE EN CURSO
# -----------------------------
class SeleccionPacienteCurso(models.Model):
    usuario = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='selecciones_paciente_curso',
        limit_choices_to={'rol': 'EST'}  # Solo estudiantes pueden seleccionar
    )

    curso = models.ForeignKey(
        Curso,
        on_delete=models.CASCADE,
        related_name='selecciones_paciente'
    )

    paciente = models.ForeignKey(
        'diagnostico_paciente.Paciente',
        on_delete=models.PROTECT,
        related_name='selecciones_en_curso'
    )

    fecha_seleccion = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('usuario', 'curso')
        verbose_name = 'Selección de paciente del curso'
        verbose_name_plural = 'Selecciones de paciente del curso'

    def __str__(self):
        return f"{self.usuario} → {self.paciente} ({self.curso})"
