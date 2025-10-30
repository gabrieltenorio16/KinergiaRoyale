from django.db import models

class Contenido(models.Model):
    titulo = models.CharField(max_length=200)
    # otros campos...

    def __str__(self):
        return self.titulo
    

class Tema(models.Model):
    titulo = models.CharField(
        max_length=150,
        null=False,
        verbose_name='Título'
    )
    descripcion = models.TextField(
        blank=True,
        verbose_name='Descripción'
    )
    estado_completado = models.BooleanField(
        default=False,
        verbose_name='Estado completado'
    )

    def __str__(self):
        return self.titulo


class Video(models.Model):
    titulo = models.CharField(
        max_length=150,
        null=False,
        verbose_name='Título'
    )
    url = models.URLField(
        max_length=300,
        null=False,
        verbose_name='URL del video'
    )
    duracion = models.PositiveIntegerField(
        null=False,
        help_text='Duración del video en segundos',
        verbose_name='Duración (segundos)'
    )
    orden = models.PositiveIntegerField(
        null=False,
        help_text='Posición del video dentro del tema',
        verbose_name='Orden'
    )

    # 🔗 Relación directa con Tema
    tema = models.ForeignKey(
        Tema,
        on_delete=models.CASCADE,   # Si se borra el tema, se borran los videos asociados
        related_name='videos',      # Permite acceder con tema.videos.all()
        verbose_name='Tema asociado'
    )

    class Meta:
        ordering = ['tema', 'orden']
        constraints = [
            models.UniqueConstraint(
                fields=['tema', 'orden'],
                name='unique_orden_por_tema'
            )
        ]

    def __str__(self):
        return f"{self.orden}. {self.titulo}"


class Pregunta(models.Model):
    contenido = models.TextField(
        null=False,
        verbose_name='Contenido de la pregunta'
    )
    orden = models.PositiveIntegerField(
        null=False,
        help_text='Posición de la pregunta dentro del video',
        verbose_name='Orden'
    )

    # 🔗 Relación directa con Video (FK video_ID en tu diagrama)
    video = models.ForeignKey(
        Video,
        on_delete=models.CASCADE,    # Si se borra el video, se borran sus preguntas
        related_name='preguntas',    # Permite acceder con video.preguntas.all()
        verbose_name='Video asociado'
    )

    class Meta:
        ordering = ['video', 'orden']
        constraints = [
            models.UniqueConstraint(
                fields=['video', 'orden'],
                name='unique_orden_por_video_en_pregunta'
            )
        ]
        verbose_name = 'Pregunta'
        verbose_name_plural = 'Preguntas'

    def __str__(self):
        return f"Pregunta {self.orden} de '{self.video.titulo}'"


class Respuesta(models.Model):
    contenido = models.TextField(
        null=False,
        verbose_name='Contenido de la respuesta'
    )
    retroalimentacion = models.TextField(
        blank=True,
        null=True,
        help_text='Explicación o feedback mostrado al estudiante después de responder',
        verbose_name='Retroalimentación'
    )
    es_correcta = models.BooleanField(
        default=False,
        verbose_name='¿Es la respuesta correcta?'
    )

    # 🔗 Relación directa con Pregunta (FK id_Pregunta en tu diagrama)
    pregunta = models.ForeignKey(
        Pregunta,
        on_delete=models.CASCADE,      # Si se borra la pregunta, se borran sus respuestas
        related_name='respuestas',     # pregunta.respuestas.all()
        verbose_name='Pregunta asociada'
    )

    class Meta:
        verbose_name = 'Respuesta'
        verbose_name_plural = 'Respuestas'

    def __str__(self):
        # corto el contenido para que el admin no explote si es largo
        contenido_preview = (self.contenido[:40] + '...') if len(self.contenido) > 40 else self.contenido
        estado = "✅" if self.es_correcta else "—"
        return f"{estado} {contenido_preview} (Pregunta {self.pregunta.orden} / Video {self.pregunta.video.titulo})"


class Estudiante(models.Model):
    nombre = models.CharField(
        max_length=150,
        null=False,
        verbose_name='Nombre del estudiante'
    )

    def __str__(self):
        return self.nombre


class FichaClinica(models.Model):
    descripcion = models.TextField(
        blank=True,
        null=True,
        verbose_name='Descripción de la ficha clínica'
    )

    def __str__(self):
        return f"Ficha {self.id}"


class Historial(models.Model):
    tema = models.ForeignKey(
        Tema,
        on_delete=models.CASCADE,
        related_name='historiales',
        verbose_name='Tema asociado'
    )
    estudiante = models.ForeignKey(
        Estudiante,
        on_delete=models.CASCADE,
        related_name='historiales',
        verbose_name='Estudiante asociado'
    )
    ficha = models.ForeignKey(
        FichaClinica,
        on_delete=models.CASCADE,
        related_name='historiales',
        verbose_name='Ficha clínica asociada'
    )

    fecha_registro = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Fecha de registro'
    )

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
        return f"Historial: {self.estudiante} / {self.tema} / Ficha {self.ficha.id}"
