from django.db import models
from django.contrib.auth.models import User
import uuid
from django.utils import timezone
from datetime import timedelta
# Create your models here.



class Cliente(models.Model):
    nombre = models.CharField(max_length=200)
    nit = models.CharField(max_length=20, unique=True, null=True, blank=True)
    direccion = models.CharField(max_length=200, blank=True)
    contacto = models.EmailField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre
    

class Profile(models.Model):
    
    class cargoChoices(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrador'
        USUARIO = 'USUARIO', 'Usuario'
        ENCUESTADOR = 'ENCUESTADOR', 'Encuestador'
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="usuarios", null=True, blank=True)

    cargo = models.CharField(max_length=100,
                             choices=cargoChoices.choices, 
                             default=cargoChoices.USUARIO)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.usuario.username} - {self.cargo} - {self.cliente}'
    
    
class InvitacionEncuestador(models.Model):
    
    
    def fecha_expiracion_default():
        return timezone.now() + timedelta(days=7)
    
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, related_name="invitaciones")
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)
    max_uso = models.PositiveIntegerField(default=1)  # puede ser más
    usado = models.PositiveIntegerField(default=0)
    expiracion = models.DateTimeField(default=fecha_expiracion_default)
    creado_por = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True, blank=True)

    def disponible(self):
        return self.usado < self.max_uso and timezone.now() < self.expiracion

    def __str__(self):
        return f"Invitación {self.token} ({self.usado}/{self.max_uso})"
    
    
    