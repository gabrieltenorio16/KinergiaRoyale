from django.db import models


class usuario(models.Model):
    Roles = [
        ('DOC', 'Docente'),
        ('EST', 'Estudiante'),
    ]

    nombre = models.CharField('Nombre', max_length=150, null=False)
    apellido = models.CharField('Apellido', max_length=150, null=False)
    correo = models.EmailField('Correo', max_length=254, null=False)
    password = models.CharField('Contraseña', max_length=128)
    rol = models.CharField('Rol', max_length=10, choices=Roles, default='EST')

    class Meta:
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'
        ordering = ('nombre', 'apellido')

    def __str__(self):
        return f"{self.id} - {self.nombre} {self.apellido} ({self.get_rol_display()})"
   