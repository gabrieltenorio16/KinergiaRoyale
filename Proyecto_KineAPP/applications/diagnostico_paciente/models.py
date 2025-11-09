from django.db import models

class Paciente(models.Model):
    nombre = models.CharField('Nombre', max_length=150)
    edad = models.PositiveIntegerField('Edad')
    avatar = models.ImageField('Avatar', upload_to='avatars/', null=True, blank=True)
    descripcion = models.CharField('Descripción', max_length=1000)

    id_modulo = models.ForeignKey(
        'curso_y_modulo.Modulo',
        on_delete=models.CASCADE,
        related_name='pacientes',
        null=True,
        blank=True
    )

    def __str__(self):
        return f"{self.id} - {self.nombre}"


class PartesDelCuerpo(models.Model):
    id_parte = models.AutoField('ID Parte', primary_key=True)
    nombre = models.CharField('Parte del cuerpo', max_length=200)
    descripcion = models.CharField('Descripción', max_length=1000)

    def __str__(self):
        return f"{self.id_parte} - {self.nombre}"


class Diagnostico(models.Model):
    descripcion = models.TextField('Descripción')
    id_paciente = models.ForeignKey(
        Paciente,
        on_delete=models.CASCADE,
        related_name='diagnosticos'
    )
    id_partes_cuerpo = models.ForeignKey(
        PartesDelCuerpo,
        on_delete=models.CASCADE,
        related_name='diagnosticos'
    )

    def __str__(self):
        return f"Diagnóstico {self.id} - Paciente: {self.id_paciente.nombre} - Parte: {self.id_partes_cuerpo.id_parte} - {self.id_partes_cuerpo.nombre}"

