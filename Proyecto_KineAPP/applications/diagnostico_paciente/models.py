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
        'Historial mdico',
        help_text='Resumen del historial mdico'
    )

    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'
        ordering = ('nombres', 'apellidos')

    def __str__(self):
        return f"{self.apellidos}, {self.nombres} (Edad: {self.edad})"


class ParteCuerpo(models.Model):
    nombre = models.CharField('Parte del cuerpo', max_length=100)
    descripcion = models.TextField('Descripci6n', blank=True)

    class Meta:
        verbose_name = 'Parte del cuerpo'
        verbose_name_plural = 'Partes del cuerpo'
        ordering = ('nombre',)

    def __str__(self):
        return self.nombre


class CasoClinico(models.Model):
    titulo = models.CharField('T2atulo del caso', max_length=150)
    descripcion = models.TextField('Descripci6n general')

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
    historial_clinico = models.TextField('Historial clnico detallado')

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Caso clnico'
        verbose_name_plural = 'Casos clnicos'
        ordering = ('-fecha_creacion', 'titulo')

    def __str__(self):
        return f"{self.titulo} - {self.paciente}"


class Etapa(models.Model):
    caso = models.ForeignKey(
        CasoClinico,
        on_delete=models.CASCADE,
        related_name='etapas',
        verbose_name='Caso clnico',
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

    # Relaci6n con el banco de preguntas de Contenido
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
        verbose_name = 'Entrevista'
        verbose_name_plural = 'Entrevistas'
        # ya no usamos "orden"
        ordering = ('caso', 'nombre')

    def __str__(self):
        return f"{self.nombre} ({self.caso.titulo})"

    @property
    def embed_url(self):
        if self.video:
            return self.video.embed_url
        return None


class Diagnostico(models.Model):
    descripcion = models.TextField(
        'Descripcion del Diagnostico',
        blank=True,
        null=True,
        help_text='Diagnostico preliminar y sugerencias de tratamiento.'
    )

    caso = models.ForeignKey(
        CasoClinico,
        on_delete=models.CASCADE,
        related_name='diagnosticos',
        verbose_name='Caso clnico',
        null= True, blank= True,
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
        verbose_name = 'Diagn0stico'
        verbose_name_plural = 'Diagnosticos'
        ordering = ('paciente',)

    def __str__(self):
        return f"Diagnostico #{self.id} de {self.paciente.apellidos}, {self.paciente.nombres}"

class FichaClinicaEstudiante (models.Model):
    # Campos de texto# 
    rut_paciente_ficha = models.CharField('RUT del Paciente', max_length=12)
    nombre_paciente_ficha = models.CharField('Nombres del Paciente', max_length=200)
    apellido_paciente_ficha = models.CharField('Apellidos del Paciente', max_length=200)
    edad_paciente_ficha = models.PositiveIntegerField('Edad del Paciente')
    anamnesis_actual = models.TextField('Anamnesis Actual')
    motivo_consulta_ficha = models.TextField('Motivo de Consulta')


    # Llaves foraneas de este modelo
    estudiante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='fichas_medicas',
        verbose_name='Estudiante'
    )

    paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='fichas_medicas_estudiantes',
        verbose_name='Paciente Simulado'
    )

    caso_clinico = models.ForeignKey(
        CasoClinico,
        on_delete=models.CASCADE,
        related_name='fichas_medicas_estudiantes',
        verbose_name='Caso Clnico'
    )

    video = models.ForeignKey(
        Video,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='fichas_medicas_estudiantes',
        verbose_name='Video Asociado'
    )

    fecha_creacion = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Ficha Clincia del Estudiante'
        verbose_name_plural = 'Fichas Clinicas de Estudiantes'
        ordering = ('-fecha_creacion',)
        constraints = [
            models.UniqueConstraint(
                fields=['estudiante', 'paciente', 'caso_clinico', 'video'],
                name='unique_ficha_estudiante_paciente_caso'
            )
        ]

    def __str__(self):
        return f"Ficha Mdica de {self.estudiante.username} para {self.paciente}"