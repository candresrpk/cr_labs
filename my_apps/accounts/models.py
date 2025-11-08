from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Profile(models.Model):
    
    class cargoChoices(models.TextChoices):
        ADMIN = 'ADMIN', 'Administrador'
        USUARIO = 'USUARIO', 'Usuario'
        ENCUESTADOR = 'ENCUESTADOR', 'Encuestador'
        
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    cargo = models.CharField(max_length=100, blank=True, choices=cargoChoices.choices, default=cargoChoices.USUARIO)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    

    def __str__(self):
        return f'Perfil de {self.user.username}, Cargo: {self.cargo}'
    
    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfiles'