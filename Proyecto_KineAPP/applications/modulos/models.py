from django.db import models

# Create your models here.

class RegistroDocente(models.Model):
    nombre=models.CharField('Nombre docente',max_length=150,null=False)
    apellido=models.CharField('Apellido docente',max_length=150,null=False)
    #rut=RUTField(unique=True)
    correo=models.EmailField('Correo',max_length=254,null=False)
    password = models.CharField('contraseña',max_length=128)

    def __str__(self):
        return str(self.id)+'-'+ self.nombre