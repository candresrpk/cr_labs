from django.db import models
from django.contrib.auth.models import User
from ..accounts.models import Profile

class Distribucion(models.Model):
    nombre = models.CharField(max_length=100)
    descripcion = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.nombre


class DatosDistribucion(models.Model):  # Usa CamelCase sin guion bajo
    class GeneroChoices(models.TextChoices):
        MASCULINO = 'MASCULINO', 'Masculino'
        FEMENINO = 'FEMENINO', 'Femenino'
        OTRO = 'OTRO', 'Otro'

    distribucion = models.ForeignKey(Distribucion, related_name='datos', on_delete=models.CASCADE)
    edad = models.PositiveIntegerField()
    genero = models.CharField(max_length=50, choices=GeneroChoices.choices)
    barrio = models.CharField(max_length=100)
    estrato = models.CharField(max_length=50)
    cuota_total = models.PositiveIntegerField(default=0)
    completadas = models.PositiveIntegerField(default=0)
    
    encuestador = models.ForeignKey(User, related_name='cuotas_asignadas', on_delete=models.SET_NULL, null=True, blank=True)
    

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.genero}, {self.edad}, {self.barrio} ({self.completadas}/{self.cuota_total})"

    @property
    def restantes(self):
        return max(self.cuota_total - self.completadas, 0)

    @property
    def progreso(self):
        return f"{self.completadas}/{self.cuota_total}"
    


class Encuesta(models.Model):
    distribucion = models.ForeignKey(Distribucion, related_name='encuestas', on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200)
    descripcion = models.TextField()
    activa = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.titulo
    
    
class PermisosEncuesta(models.Model):
    encuesta = models.ForeignKey(Encuesta, related_name='permisos', on_delete=models.CASCADE)
    usuario = models.ForeignKey(Profile, related_name='permisos_encuestas', on_delete=models.CASCADE)
    puede_editar = models.BooleanField(default=False)
    
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
    clase = models.CharField(max_length=50, choices=ClasesPregunta.choices, default=ClasesPregunta.OPCION_MULTIPLE)
    texto = models.CharField(max_length=300)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.texto
    

class Opcion(models.Model):
    pregunta = models.ForeignKey(Pregunta, related_name='opciones', on_delete=models.CASCADE)
    texto = models.CharField(max_length=200)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.opcion
    

class Respuesta(models.Model):
    encuesta = models.ForeignKey(Encuesta, related_name='respuestas', on_delete=models.CASCADE)
    encuestador = models.ForeignKey(User, related_name='respuestas', on_delete=models.SET_NULL, null=True)
    
    edad = models.IntegerField()
    genero = models.CharField(max_length=50)
    barrio = models.CharField(max_length=100) 
    estrato = models.CharField(max_length=50)

    opcion = models.ForeignKey(Opcion, related_name='respuestas', on_delete=models.SET_NULL, null=True, blank=True)
    texto_libre = models.TextField(null=True, blank=True)
    
    latitud = models.FloatField(null=True, blank=True)
    longitud = models.FloatField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.pregunta.texto}: {self.texto or self.opcion}"
