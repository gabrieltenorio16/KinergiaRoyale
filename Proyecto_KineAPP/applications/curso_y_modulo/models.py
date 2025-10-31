from django.db import models

# Create your models here.

# Clase Curso
class Curso(models.Model):

    nivel_choices = [
        ('BASICO', 'Básico'),
        ('INTERMEDIO', 'Intermedio'),
        ('AVANZADO', 'Avanzado'),
    ]

    nivel = models.CharField(
        max_length=10, 
        choices=nivel_choices, 
        default='BASICO')

    nombre = models.CharField(max_length=100)
    docente = models.ForeignKey(
        'Docente', 
        on_delete=models.SET_NULL,
        null=True,
        related_name='cursos_docente'
    )

    usuario = models.ForeignKey(
        'usuario.usuario',
        on_delete=models.SET_NULL,
        null=True,
        related_name='cursos_usuario'
    )

    def __str__(self):
        return f"{self.id} - {self.nombre} ({self.get_nivel_display()})" 

#Clase Modulos
class Modulo(models.Model):
    nombre = models.CharField(max_length=100)
    curso = models.ForeignKey(
        'Curso', 
        on_delete=models.CASCADE,
        related_name='modulos'
    )

    def __str__(self):
        return f"{self.id} - {self.nombre}"

#Clase Docente
class Docente(models.Model):
    nombre = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.id} - {self.nombre}"

#Clase Contenido Adicional
class ContenidoAdicional(models.Model):
    nombre = models.CharField(max_length=100)
    tipo_archivo = models.CharField(max_length=100)
    url = models.URLField(max_length=500)
    directorio = models.CharField(max_length=500)
    modulo = models.ForeignKey(
        Modulo,
        on_delete=models.CASCADE,
        related_name='contenido_adicional')

    def __str__(self):
        return f"{self.id} - {self.nombre}"

