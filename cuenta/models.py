from django.contrib.auth.models import AbstractUser
from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=255)
    direccion = models.TextField( null=True, blank=True, default= None ) 
    telefono = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField( null=True, blank=True ) 
    fecha_creacion = models.DateTimeField(auto_now_add=True, null=True, blank=True)

    def __str__(self):
        return self.nombre

class Cuenta(AbstractUser):
    cliente = models.ForeignKey('Cliente', on_delete=models.CASCADE, default=None, null=True, blank=True)
    foto = models.CharField(max_length=255)

    def __str__(self):
        return self.username

class Rol(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()
    cuentas = models.ManyToManyField(Cuenta)

class RolPermiso(models.Model):
    rol = models.ForeignKey('Rol', on_delete=models.CASCADE)
    permiso = models.ForeignKey('Permiso', on_delete=models.CASCADE)

class Permiso(models.Model):
    nombre = models.CharField(max_length=255)
    descripcion = models.TextField()