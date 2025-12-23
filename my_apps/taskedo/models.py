from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Task(models.Model):
    owner = models.ForeignKey(User, related_name='tasks', 
                              on_delete=models.CASCADE, 
                              verbose_name='Propietario'
                              )
    title = models.CharField(max_length=200, verbose_name='Título')
    description = models.TextField(verbose_name='Descripción')
    completed = models.BooleanField(default=False, verbose_name='Completado')
    
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Creado')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Actualizado')
    
    class Meta:
        verbose_name = 'Tarea'
        verbose_name_plural = 'Tareas'
        ordering = ['completed']
        
        
    def get_all_completed(self):
        return self.objects.filter(completed=True)
    
    
    def __str__(self):
        return self.title
    
    
