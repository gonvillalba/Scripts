from django.db import models

# Create your models here.
class Libro(models.Model):
    titulo = models.CharField(max_length=150)
    autor = models.CharField(max_length=150)
    genero = models.CharField(max_length=100)
    year_publication = models.DateField()

class Usuario(models.Model):
    TIPO_USUARIOS = (
        ('normal', 'Normal' ),
        ('admin', 'Admin')
    )
    nombre = models.CharField(max_length=150)
    email = models.EmailField()
    tipo_usuario = models.CharField(max_length= 6, choices= TIPO_USUARIOS, default= 'normal')

class Prestamo(models.Model):
    ESTADO =(
        ('activo', 'Activo'),
        ('devuelto','Devuelto')
    )
    libro = models.ForeignKey(Libro)
    usuario = models.ForeignKey(Usuario)
    fecha_prestamo = models.DateField()
    fecha_devolucion = models.DateField()
    estado = models.CharField(max_length=8, choices=ESTADO , default= 'devuelto')