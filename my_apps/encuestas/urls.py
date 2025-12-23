from django.urls import path
from . import views

app_name = 'encuestas'


urlpatterns = [
    path('', views.encuestasListView, name='list'),
    path('crear/', views.crearEncuestaView, name='crear'),
    path('distribucion/crear/', views.crearDistribucionView, name='crear_distribucion'),
    path('detalle/<int:encuesta_id>/', views.encuestaDetailView, name='detalle'),
]