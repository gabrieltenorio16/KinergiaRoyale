from django.db import models
from django.conf import settings
from urllib.parse import urlparse, parse_qs

class Topico(models.Model):
    nombre = models.CharField('Nombre del tópico', max_length=100, unique=True)
    descripcion = models.TextField('Descripción', blank=True)

    class Meta:
        verbose_name = 'Tópico'
        verbose_name_plural = 'Tópicos'
        ordering = ['nombre']

    def __str__(self):
        return self.nombre

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
    pregunta = models.TextField(verbose_name='Pregunta')
    topico = models.ForeignKey(
        Topico,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='preguntas',
        verbose_name='Tópico',
    )

    class Meta:
        verbose_name = 'Pregunta'
        verbose_name_plural = 'Preguntas'
        ordering = ['id']

    def __str__(self):
        return self.pregunta[:60]

class Respuesta(models.Model):
    contenido = models.TextField(verbose_name='Contenido de la respuesta')
    retroalimentacion = models.TextField(
        blank=True,
        null=True,
        verbose_name='Retroalimentación',
        help_text='Explicación mostrada al estudiante',
    )
    es_correcta = models.BooleanField(default=False, verbose_name='¿Es la respuesta correcta?')

    pregunta = models.ForeignKey(
        Pregunta,
        on_delete=models.CASCADE,
        related_name='respuestas',
        verbose_name='Pregunta asociada',
    )

    class Meta:
        verbose_name = 'Respuesta'
        verbose_name_plural = 'Respuestas'
        ordering = ['pregunta', 'id']

    def __str__(self):
        preview = (self.contenido[:40] + '...') if len(self.contenido) > 40 else self.contenido
        estado = "✔" if self.es_correcta else "-"
        return f"{estado} {preview}"
