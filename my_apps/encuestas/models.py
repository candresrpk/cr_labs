from django.db import models
from django.contrib.auth.models import User

class Distribucion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre


class Datos_Distribucion(models.Model):
    
    class GeneroChoices(models.TextChoices):
        MASCULINO = 'MASCULINO', 'Masculino'
        FEMENINO = 'FEMENINO', 'Femenino'
        OTRO = 'OTRO', 'Otro'
    
    distribucion = models.ForeignKey(Distribucion, related_name='datos_distribucion', on_delete=models.CASCADE)
    edad = models.IntegerField()
    genero = models.CharField(max_length=50, choices=GeneroChoices.choices, default=GeneroChoices.OTRO)
    barrio = models.CharField(max_length=100)
    estrato = models.CharField(max_length=50)
    encuestador = models.ForeignKey(User, related_name='datos_distribucion_asignados', on_delete=models.SET_NULL, null=True, blank=True)
    
        
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.clave}: {self.valor}"    
    


class Encuesta(models.Model):
    distribucion = models.ForeignKey(Distribucion, related_name='encuestas', on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo
    
    
class PermisosEncuesta(models.Model):
    encuesta = models.ForeignKey(Encuesta, related_name='permisos', on_delete=models.CASCADE)
    usuario = models.ForeignKey(User, related_name='permisos_encuestas', on_delete=models.CASCADE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Permiso de {self.usuario.username} para {self.encuesta.titulo} "


class Pregunta(models.Model):
    
    class ClasesPregunta(models.TextChoices):
        OPCION_MULTIPLE = 'OPCION_MULTIPLE', 'Opción Múltiple'
        RESPUESTA_CORTA = 'RESPUESTA_CORTA', 'Respuesta Corta'
        RESPUESTA_LARGA = 'RESPUESTA_LARGA', 'Respuesta Larga'
        
    
    encuesta = models.ForeignKey(Encuesta, related_name='preguntas', on_delete=models.CASCADE)
    clase = models.CharField(max_length=100)
    pregunta = models.CharField(max_length=300, null=False, blank=False, default=ClasesPregunta.OPCION_MULTIPLE)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.pregunta
    

class Opcion(models.Model):
    pregunta = models.ForeignKey(Pregunta, related_name='opciones', on_delete=models.CASCADE)
    opcion = models.CharField(max_length=200)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.opcion
    

class Respuesta(models.Model):
    opcion = models.ForeignKey(Opcion, related_name='respuestas', on_delete=models.CASCADE)
    latitud = models.FloatField()
    longitud = models.FloatField()
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Respuesta a {self.opcion.texto} en {self.fecha_hora}"