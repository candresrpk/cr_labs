from django.urls import path
from my_apps.taskedo import views

app_name = 'taskedo'

urlpatterns = [
    path('', views.TasksHomeView.as_view(), name='home'),
    path('list/', views.ListTasksView.as_view(), name='list'),
    path('crear/', views.CreateTaskView.as_view(), name='create'),
    path('eliminar/<int:pk>/', views.TaskDeleteView.as_view(), name='delete'),
    # path('detalle/<int:pk>/', views.DetailTaskView.as_view(), name='detail'),
]