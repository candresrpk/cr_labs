from django.urls import path
from my_apps.taskedo import views

app_name = 'taskedo'

urlpatterns = [
    path('', views.TasksHomeView.as_view(), name='home'),
]