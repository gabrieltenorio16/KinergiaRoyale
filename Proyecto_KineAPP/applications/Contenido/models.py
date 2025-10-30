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
