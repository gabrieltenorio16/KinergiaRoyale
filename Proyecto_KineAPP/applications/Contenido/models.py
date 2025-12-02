from django.db import models
from django.conf import settings
from urllib.parse import urlparse, parse_qs

class Contenido(models.Model):
    titulo = models.CharField(max_length=200)

    def __str__(self):
        return self.titulo


class Tema(models.Model):
    titulo = models.CharField(max_length=150, null=False, verbose_name='Título')
    descripcion = models.TextField(blank=True, verbose_name='Descripción')
    estado_completado = models.BooleanField(default=False, verbose_name='Estado completado')
    fecha_inicio = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de inicio')
    fecha_fin = models.DateTimeField(null=True, blank=True, verbose_name='Fecha de finalización')

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
    titulo = models.CharField(max_length=150, null=False)
    url = models.URLField(max_length=300, null=False)

    tema = models.ForeignKey('Tema', on_delete=models.CASCADE)

    def __str__(self):
        return self.titulo

    @property
    def embed_url(self):
        """
        Devuelve una URL embebible para YouTube (incluye shorts/watch/embed)
        usando siempre https://www.youtube-nocookie.com.
        Si la URL no es de YouTube, devuelve la URL original.
        """
        if not self.url:
            return ""

        parsed = urlparse(self.url)
        netloc = parsed.netloc.lower()
        path = parsed.path

        def build_embed(video_id: str, extra_params: str = "") -> str:
            if extra_params:
                return f"https://www.youtube-nocookie.com/embed/{video_id}?{extra_params}"
            return f"https://www.youtube-nocookie.com/embed/{video_id}"

        # URLs tipo youtu.be/<id>
        if "youtu.be" in netloc:
            video_id = path.lstrip("/")
            params = parsed.query
            return build_embed(video_id, params)

        # URLs tipo /watch?v=<id>
        if "youtube" in netloc and "watch" in path:
            qs = parse_qs(parsed.query)
            video_id = qs.get("v", [""])[0]
            params = "&".join(f"{k}={v[0]}" for k, v in qs.items() if k != "v")
            return build_embed(video_id, params)

        # URLs tipo /shorts/<id>
        if "youtube" in netloc and "/shorts/" in path:
            video_id = path.split("/shorts/")[-1].split("/")[0]
            params = parsed.query
            return build_embed(video_id, params)

        # URLs que ya vienen en /embed/...
        if "youtube" in netloc and "embed" in path:
            # Aseguramos https y dominio nocookie
            return f"https://www.youtube-nocookie.com{path}" + (f"?{parsed.query}" if parsed.query else "")

        # Fallback: devolver la URL tal cual (para otros proveedores)
        return self.url

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
