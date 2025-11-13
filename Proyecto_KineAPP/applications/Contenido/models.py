from django.db import models
from django.conf import settings


class Contenido(models.Model):
    titulo = models.CharField(max_length=200)

    def __str__(self):
        return self.titulo


class Tema(models.Model):
    titulo = models.CharField(max_length=150, null=False, verbose_name='Título')
    descripcion = models.TextField(blank=True, verbose_name='Descripción')
    estado_completado = models.BooleanField(default=False, verbose_name='Estado completado')

    # AHORA: ligar el tema directamente a un CURSO (ya no usamos Modulo)
    curso = models.ForeignKey(
        'curso_y_modulo.Curso',
        on_delete=models.PROTECT,
        null=True,
        blank=True,
        related_name='temas',
        verbose_name='Curso asociado'
    )

    class Meta:
        verbose_name = 'Tema'
        verbose_name_plural = 'Temas'
        ordering = ['titulo']

    def __str__(self):
        if self.curso:
            return f"{self.titulo} ({self.curso})"
        return self.titulo


class Video(models.Model):
    titulo = models.CharField(max_length=150, null=False, verbose_name='Título')
    url = models.URLField(max_length=300, null=False, verbose_name='URL del video')

    tema = models.ForeignKey(
        'Tema',
        on_delete=models.CASCADE,
        related_name='videos',
        verbose_name='Tema asociado'
    )

    class Meta:
        ordering = ['tema', 'id']

    def __str__(self):
        return f"{self.titulo}"


class Pregunta(models.Model):
    contenido = models.TextField(null=False, verbose_name='Contenido de la pregunta')

    video = models.ForeignKey(
        'Video',
        on_delete=models.CASCADE,
        related_name='preguntas',
        verbose_name='Video asociado'
    )

    # OPCIONAL: orden de la pregunta dentro del video
    orden = models.PositiveIntegerField(
        'Orden',
        default=1,
        help_text='Orden de la pregunta dentro del video'
    )

    class Meta:
        ordering = ['video', 'orden']
        verbose_name = 'Pregunta'
        verbose_name_plural = 'Preguntas'
        unique_together = ('video', 'orden')

    def __str__(self):
        return f"{self.video.titulo} - P{self.orden}: {self.contenido[:40]}"


class Buscador_de_respuesta(models.Model):
    contenido = models.TextField(null=False, verbose_name='Contenido de la respuesta')
    retroalimentacion = models.TextField(
        blank=True, null=True, verbose_name='Retroalimentación',
        help_text='Explicación mostrada al estudiante'
    )
    es_correcta = models.BooleanField(default=False, verbose_name='¿Es la respuesta correcta?')

    pregunta = models.ForeignKey(
        'Pregunta',
        on_delete=models.CASCADE,
        related_name='respuestas',
        verbose_name='Pregunta asociada'
    )

    class Meta:
        verbose_name = 'Respuesta'
        verbose_name_plural = 'Respuestas'
        ordering = ['pregunta', 'id']

    def __str__(self):
        preview = (self.contenido[:40] + '...') if len(self.contenido) > 40 else self.contenido
        estado = "✅" if self.es_correcta else "—"
        return f"{estado} {preview} (Video {self.pregunta.video.titulo})"


class FichaClinica(models.Model):
    descripcion = models.TextField(blank=True, null=True, verbose_name='Descripción de la ficha clínica')

    # OPCIONAL: enganchar con un caso clínico del otro modelo
    caso_clinico = models.ForeignKey(
        'diagnostico_paciente.CasoClinico',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='fichas_contenido',
        verbose_name='Caso clínico asociado'
    )

    class Meta:
        verbose_name = 'Ficha clínica'
        verbose_name_plural = 'Fichas clínicas'

    def __str__(self):
        if self.caso_clinico:
            return f"Ficha {self.id} - {self.caso_clinico.titulo}"
        return f"Ficha {self.id}"


class Historial(models.Model):
    tema = models.ForeignKey(
        'Tema',
        on_delete=models.CASCADE,
        related_name='historiales',
        verbose_name='Tema asociado'
    )
    estudiante = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='historiales',
        verbose_name='Estudiante asociado',
        limit_choices_to={'rol': 'EST'},  # solo estudiantes
    )
    ficha = models.ForeignKey(
        'FichaClinica',
        on_delete=models.CASCADE,
        related_name='historiales',
        verbose_name='Ficha clínica asociada'
    )

    fecha_registro = models.DateTimeField(auto_now_add=True, verbose_name='Fecha de registro')

    class Meta:
        verbose_name = 'Historial'
        verbose_name_plural = 'Historiales'
        ordering = ['-fecha_registro']
        constraints = [
            models.UniqueConstraint(
                fields=['tema', 'estudiante', 'ficha'],
                name='unique_tema_estudiante_ficha'
            )
        ]

    def __str__(self):
        return f"Historial: {self.estudiante} / {self.tema} / Ficha {self.ficha_id}"
