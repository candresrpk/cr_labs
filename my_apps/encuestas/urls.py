from django.urls import path
from . import views

app_name = 'encuestas'


urlpatterns = [
    path('', views.home, name='dashboard'),
]