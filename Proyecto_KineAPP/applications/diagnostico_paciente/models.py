from django.db import models
from django.conf import settings
from urllib.parse import urlparse, parse_qs ###


class Paciente(models.Model):
    nombres = models.CharField('Nombres', max_length=100)
    apellidos = models.CharField('Apellidos', max_length=100)
    edad = models.PositiveIntegerField('Edad')
    antecedentes = models.TextField('Antecedentes', help_text='Antecedentes relevantes del paciente')
    historial_medico = models.TextField('Historial médico', help_text='Resumen del historial médico')

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

    # Mantengo solo el curso
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

    # 2. Conexión al Paciente (¡AQUÍ ESTÁ LA CLAVE!)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE, related_name='etapas_asociadas')

    nombre = models.CharField('Nombre de la etapa', max_length=150)
    orden = models.PositiveIntegerField(
        'Orden',
        default=1,
        help_text='Orden de la etapa dentro del caso clínico'
    )

    parte_cuerpo = models.ForeignKey(
        ParteCuerpo,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='etapas',
        verbose_name='Parte del cuerpo relacionada',
    )

    pregunta = models.TextField(
        'Pregunta o enunciado',
        help_text='Pregunta principal de esta etapa'
    )
    url_video = models.URLField(
        'Video asociado (URL)',
        max_length=300,
        blank=True,
        null=True
    )

    ####
    @property
    def embed_url(self):
        url = self.url_video # <--- ESTO ESTÁ BIEN, SE MANTIENE
        if not url: return None
        
        parsed = urlparse(url)

        # Caso 1: URL corta youtu.be
        if "youtu.be" in parsed.netloc:
            video_id = parsed.path.lstrip("/")
            params = parsed.query
            if params:
                # CAMBIO: Usamos 'https' y 'youtube-nocookie'
                return f"//www.youtube-nocookie.com/embed/{video_id}?{params}"
            return f"//www.youtube-nocookie.com/embed/{video_id}"

        # Caso 2: watch?v=ID
        if "watch" in parsed.path:
            qs = parse_qs(parsed.query)
            video_id = qs.get("v", [""])[0]
            params = "&".join(
                f"{k}={v[0]}" for k, v in qs.items() if k != "v"
            )
            if params:
                # CAMBIO: Usamos 'https' y 'youtube-nocookie'
                return f"//www.youtube-nocookie.com/embed/{video_id}?{params}"
            return f"//www.youtube-nocookie.com/embed/{video_id}"

        # Caso 3: /embed/
        if "embed" in parsed.path:
            return url

        return url
    ####

    # NUEVO: contenido adicional opcional (lo que antes iba a Modulo/ContenidoAdicional)
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
        ordering = ('caso', 'orden')
        unique_together = ('caso', 'orden')

    def __str__(self):
        return f"Etapa {self.orden} - {self.nombre} ({self.caso.titulo})"


class TipoRespuesta(models.Model):
    nombre = models.CharField('Tipo de respuesta', max_length=50)
    descripcion = models.TextField('Descripción', blank=True)

    class Meta:
        verbose_name = 'Tipo de respuesta'
        verbose_name_plural = 'Tipos de respuesta'
        ordering = ('nombre',)

    def __str__(self):
        return self.nombre


class Respuesta(models.Model):
    etapa = models.ForeignKey(
        Etapa,
        on_delete=models.CASCADE,
        related_name='respuestas',
        verbose_name='Etapa asociada',
    )
    tipo = models.ForeignKey(
        TipoRespuesta,
        on_delete=models.PROTECT,
        related_name='respuestas',
        verbose_name='Tipo de respuesta',
    )

    contenido = models.TextField('Contenido de la respuesta')
    es_correcta = models.BooleanField('¿Es la respuesta correcta?', default=False)
    retroalimentacion = models.TextField(
        'Retroalimentación',
        blank=True,
        help_text='Texto que se muestra al estudiante después de responder'
    )

    class Meta:
        verbose_name = 'Respuesta'
        verbose_name_plural = 'Respuestas'
        ordering = ('etapa', 'id')

    def __str__(self):
        preview = (self.contenido[:40] + '...') if len(self.contenido) > 40 else self.contenido
        estado = "✅" if self.es_correcta else "—"
        return f"{estado} {preview} (Etapa {self.etapa.orden} - {self.etapa.caso.titulo})"


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

# Asegúrate de que el modelo 'PartesCuerpo' sea accesible
# from .models import Paciente, PartesCuerpo 
#MODELODIAGNOSTICONUEVO
class Diagnostico(models.Model):
    descripcion = models.TextField(
        'Descripción del Diagnóstico',
        blank=True,
        null=True,
        help_text='Diagnóstico preliminar y sugerencias de tratamiento.'
    ) 
    
    # --- CAMPO FALTANTE: PARTE DEL CUERPO (Relación 1:N) ---
    parte_cuerpo = models.ForeignKey(
        'ParteCuerpo', # Referencia a la clase ParteCuerpo
        on_delete=models.SET_NULL, # Si se borra la ParteCuerpo, se pone NULL
        related_name='diagnosticos_en_parte',
        verbose_name='Parte del Cuerpo Afectada',
        blank=True,
        null=True
    )
    
    paciente = models.ForeignKey(
        'Paciente',
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