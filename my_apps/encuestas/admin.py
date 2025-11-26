from django.contrib import admin
from .models import (
    Distribucion,
    DatosDistribucion,
    Encuesta,
    PermisosEncuesta,
    Pregunta,
    Opcion,
    Respuesta
)

# =====================================================
#               ADMIN CONFIGURACIONES
# =====================================================

@admin.register(Distribucion)
class DistribucionAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion', 'created_at', 'updated_at')
    search_fields = ('nombre',)
    list_filter = ('created_at',)


@admin.register(DatosDistribucion)
class DatosDistribucionAdmin(admin.ModelAdmin):
    list_display = ('distribucion', 'edad', 'genero', 'barrio', 'estrato', 'encuestador', 'completadas', 'cuota_total')
    list_filter = ('distribucion', 'genero', 'barrio', 'estrato')
    search_fields = ('barrio', 'encuestador__user__username')
    readonly_fields = ('completadas',)


@admin.register(Encuesta)
class EncuestaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'distribucion', 'descripcion', 'created_at')
    search_fields = ('titulo', 'descripcion')
    list_filter = ('distribucion',)


@admin.register(PermisosEncuesta)
class PermisosEncuestaAdmin(admin.ModelAdmin):
    list_display = ('encuesta', 'usuario', 'created_at')
    search_fields = ('usuario__user__username', 'encuesta__titulo')
    list_filter = ('encuesta',)


@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
    list_display = ('texto', 'encuesta', 'clase', 'created_at')
    search_fields = ('texto',)
    list_filter = ('encuesta', 'clase')


@admin.register(Opcion)
class OpcionAdmin(admin.ModelAdmin):
    list_display = ('texto', 'pregunta', 'created_at')
    search_fields = ('texto',)
    list_filter = ('pregunta',)


@admin.register(Respuesta)
class RespuestaAdmin(admin.ModelAdmin):
    list_display = ('encuesta', 'encuestador', 'edad', 'genero', 'barrio', 'estrato', 'created_at')
    search_fields = ('encuestador__user__username', 'barrio')
    list_filter = ('encuesta', 'genero', 'barrio', 'estrato')
