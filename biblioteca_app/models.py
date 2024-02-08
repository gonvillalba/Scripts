from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Libro(models.Model):
    titulo = models.CharField(max_length=150)
    autor = models.CharField(max_length=150)
    genero = models.CharField(max_length=50)
    year_publication = models.DateField()

class Usuario(AbstractUser):
    TIPO_USUARIOS = (
        ('normal', 'Normal' ),
        ('admin', 'Admin')
    )
    tipo_usuario = models.CharField(max_length= 6, choices= TIPO_USUARIOS, default= 'normal')
    permissions = models.ManyToManyField('auth.Permission', blank=True, related_name='usuarios_permissions')
    groups = models.ManyToManyField('auth.Group', blank=True, related_name='usuarios_groups')  
    user_permissions = models.ManyToManyField('auth.Permission', blank=True, related_name='usuarios_user_permissions')      


class Prestamo(models.Model):
    ESTADO =(
        ('activo', 'Activo'),
        ('devuelto','Devuelto')
    )
    libro = models.ForeignKey(Libro, on_delete=models.CASCADE)
    usuario = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_prestamo = models.DateField()
    fecha_devolucion = models.DateField()
    estado = models.CharField(max_length=8, choices=ESTADO , default= 'devuelto')