from django.db import models
from django.conf import settings  # usa AUTH_USER_MODEL


class Curso(models.Model):
    NIVEL_CHOICES = [
        ('BASICO', 'Básico'),
        ('INTERMEDIO', 'Intermedio'),
        ('AVANZADO', 'Avanzado'),
    ]

    nivel = models.CharField('Nivel', max_length=10, choices=NIVEL_CHOICES, default='BASICO')
    nombre = models.CharField('Nombre', max_length=100)

    # NUEVOS (reemplazan a los FK antiguos 'docente' y 'usuario')
    docentes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='cursos_como_docente',
        blank=True,
        verbose_name='Docentes',
    )
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
        return f"{self.id} - {self.nombre} ({self.get_nivel_display()})"


class Modulo(models.Model):
    nombre = models.CharField('Nombre', max_length=100)
    curso = models.ForeignKey(
        Curso,
        on_delete=models.CASCADE,
        related_name='modulos',
        verbose_name='Curso',
    )

    class Meta:
        verbose_name = 'Módulo'
        verbose_name_plural = 'Módulos'
        ordering = ('curso', 'nombre')

    def __str__(self):
        return f"{self.id} - {self.nombre}"


class ContenidoAdicional(models.Model):
    nombre = models.CharField('Nombre', max_length=100)
    tipo_archivo = models.CharField('Tipo de archivo', max_length=100)
    url = models.URLField('URL', max_length=500)
    directorio = models.CharField('Directorio', max_length=500)
    modulo = models.ForeignKey(
        Modulo,
        on_delete=models.CASCADE,
        related_name='contenido_adicional',
        verbose_name='Módulo',
    )

    class Meta:
        verbose_name = 'Contenido adicional'
        verbose_name_plural = 'Contenidos adicionales'
        ordering = ('modulo', 'nombre')

    def __str__(self):
        return f"{self.id} - {self.nombre}"
