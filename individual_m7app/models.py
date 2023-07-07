from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Etiqueta(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Prioridad(models.Model):
    OPCIONES_PRIORIDAD = (
        (1, 'Prioridad Alta'),
        (2, 'Prioridad Normal'),
        (3, 'Prioridad Baja'),
    )

    nombre = models.CharField(max_length=20, choices=OPCIONES_PRIORIDAD)
    orden = models.IntegerField(unique=True)

    class Meta:
        ordering = ['orden']

    def __str__(self):
        return self.nombre

class Task(models.Model):
    STATUS_CHOICES = (
        ('pendiente', 'Pendiente'),
        ('en_progreso', 'En progreso'),
        ('completada', 'Completada'),
    )

    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    fecha_limite = models.DateField()
    estado = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendiente')
    etiqueta = models.ForeignKey(Etiqueta, on_delete=models.SET_NULL, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    observacion = models.TextField(max_length=200, blank=True, null=True)
    prioridad = models.ForeignKey(Prioridad, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.title
    
