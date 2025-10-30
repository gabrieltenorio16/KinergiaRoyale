from django.db import models

# Create your models here.

class usuario(models.Model):
    Roles = [
        ('ADM', 'Administrador'),
        ('Doc', 'Docente'),
        ('EST', 'Estudiante'),
    ]

    nombre=models.CharField('Nombre',max_length=150,null=False)
    apellido=models.CharField('Apellido',max_length=150,null=False)
    #rut=RUTField(unique=True)
    correo=models.EmailField('Correo',max_length=254,null=False)
    password = models.CharField('contraseña',max_length=128)
    rol = models.CharField('Rol', max_length=10, choices=Roles)


    #def __str__(self):
     #   return str(self.id)+'-'+ self.nombre # Este bloque es el anterior, la nueva es más visual.
    
    def __str__(self):
        return f"{self.id} - {self.nombre} ({self.get_rol_display()})"
