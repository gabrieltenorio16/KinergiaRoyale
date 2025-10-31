from django.db import models

# Create your models here.

class Paciente(models.Model):
    nombre = models.CharField('Nombre', max_length=150, null=False)
    edad = models.PositiveIntegerField('Edad', null=False)
    avatar = models.ImageField('Avatar', upload_to='avatars/', null=True, blank=True)
    descripcion = models.CharField('Descripción', max_length=1000, null=False)
    
    # id_tema = models.ForeignKey('Tema', on_delete=models.CASCADE, related_name='pacientes')
    # id_modulo = models.ForeignKey('Modulo', on_delete=models.CASCADE, related_name='pacientes')

    def __str__(self):
        return f"{self.id} - {self.nombre}"

    
