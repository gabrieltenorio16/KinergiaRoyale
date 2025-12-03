from django.db import models
from django.conf import settings

from applications.Contenido.models import Video, Pregunta  # Importamos Video y Pregunta


class Paciente(models.Model):
    nombres = models.CharField('Nombres', max_length=100)
    apellidos = models.CharField('Apellidos', max_length=100)
    edad = models.PositiveIntegerField('Edad')
    antecedentes = models.TextField(
        'Antecedentes',
        help_text='Antecedentes relevantes del paciente'
    )
    historial_medico = models.TextField(
        'Historial médico',
        help_text='Resumen del historial médico'
    )

    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
        ordering = ('apellidos', 'nombres')

    def __str__(self):
        return f"{self.apellidos}, {self.nombres} (Edad: {self.edad})"


class ParteCuerpo(models.Model):
    nombre = models.CharField('Parte del cuerpo', max_length=100)
    descripcion = models.TextField('Descripción', blank=True)

    class Meta:
        verbose_name = 'Parte del cuerpo'
        verbose_name_plural = 'Partes del cuerpo'
        ordering = ('nombre',)

    def __str__(self):
        return self.nombre


class CasoClinico(models.Model):
    titulo = models.CharField('Título del caso', max_length=150)
    descripcion = models.TextField('Descripción general')

    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='casos_clinicos',
        verbose_name='Paciente',
    )

    curso = models.ForeignKey(
        'curso_y_modulo.Curso',
        on_delete=models.PROTECT,
        related_name='casos_clinicos',
        verbose_name='Curso asociado',
    )

    motivo_consulta = models.TextField('Motivo de consulta')
    antecedentes = models.TextField('Antecedentes del caso')
    historial_clinico = models.TextField('Historial clínico detallado')

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Caso clínico'
        verbose_name_plural = 'Casos clínicos'
        ordering = ('-fecha_creacion', 'titulo')

    def __str__(self):
        return f"{self.titulo} - {self.paciente}"


class Etapa(models.Model):
    caso = models.ForeignKey(
        CasoClinico,
        on_delete=models.CASCADE,
        related_name='etapas',
        verbose_name='Caso clínico',
    )

    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='etapas_asociadas'
    )

    nombre = models.CharField('Nombre de la etapa', max_length=150)

    parte_cuerpo = models.ForeignKey(
        ParteCuerpo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='etapas',
        verbose_name='Parte del cuerpo relacionada',
    )

    # Relación con el banco de preguntas de Contenido
    preguntas = models.ManyToManyField(
        Pregunta,
        related_name='etapas',
        blank=True,
        verbose_name='Preguntas disponibles para esta etapa'
    )

    # Video opcional
    video = models.ForeignKey(
        Video,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='etapas',
        verbose_name='Video asociado',
    )

    contenido_adicional_url = models.URLField(
        'Contenido adicional (URL)',
        max_length=500,
        blank=True,
        help_text='Opcional'
    )
    contenido_adicional_archivo = models.FileField(
        'Contenido adicional (archivo)',
        upload_to='contenidos_adicionales/',
        blank=True,
        null=True
    )

    class Meta:
        verbose_name = 'Etapa'
        verbose_name_plural = 'Etapas'
        # ya no usamos "orden"
        ordering = ('caso', 'nombre')

    def __str__(self):
        return f"{self.nombre} ({self.caso.titulo})"

    @property
    def embed_url(self):
        if self.video:
            return self.video.embed_url
        return None


class HistorialCurso(models.Model):
    curso = models.ForeignKey(
        'curso_y_modulo.Curso',
        on_delete=models.CASCADE,
        related_name='historiales_curso',
        verbose_name='Curso'
    )
    estudiante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='historiales_curso',
        verbose_name='Estudiante',
        limit_choices_to={'rol': 'EST'},
    )
    fecha_inicio = models.DateTimeField('Fecha de inicio', auto_now_add=True)

    class Meta:
        verbose_name = 'Historial de curso'
        verbose_name_plural = 'Historiales de curso'
        unique_together = ('curso', 'estudiante')

    def __str__(self):
        return f"{self.estudiante} en {self.curso}"


class Diagnostico(models.Model):
    descripcion = models.TextField(
        'Descripción del Diagnóstico',
        blank=True,
        null=True,
        help_text='Diagnóstico preliminar y sugerencias de tratamiento.'
    )

    parte_cuerpo = models.ForeignKey(
        ParteCuerpo,
        on_delete=models.SET_NULL,
        related_name='diagnosticos_en_parte',
        verbose_name='Parte del Cuerpo Afectada',
        blank=True,
        null=True
    )

    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='diagnosticos',
        verbose_name='Paciente'
    )

    class Meta:
        verbose_name = 'Diagnóstico'
        verbose_name_plural = 'Diagnósticos'
        ordering = ('paciente',)

    def __str__(self):
        return f"Diagnóstico #{self.id} de {self.paciente.apellidos}, {self.paciente.nombres}"
