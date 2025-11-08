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

    # Añadido: Un curso puede tener varios estudiantes
    estudiantes = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='cursos_como_estudiante',
        blank=True,
        verbose_name='Estudiantes',
    )

    # Un curso puede tener varios módulos (temas de aprendizaje)
    modulos = models.ManyToManyField(
        'Modulo',
        related_name='cursos',
        blank=True,
        verbose_name='Módulos asignados',
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
# MÓDULO
# -----------------------------
class Modulo(models.Model):
    nombre = models.CharField('Nombre del módulo', max_length=100)
    descripcion = models.TextField('Descripción', blank=True, null=True)
    imagen = models.ImageField('Imagen del módulo', upload_to='modulos/', blank=True, null=True)

    class Meta:
        verbose_name = 'Módulo'
        verbose_name_plural = 'Módulos'
        ordering = ('nombre',)

    def __str__(self):
        return self.nombre


# -----------------------------
# CONTENIDO ADICIONAL
# -----------------------------
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
        return f"{self.nombre} ({self.modulo})"

